import pandas as pd
from datetime import datetime, timedelta, date
import pendulum
import os

from square.client import Square
from square.environment import SquareEnvironment

from config.Config_loader import load_config
from engineering.square.Structures import item_list_count, modifier_list_count, sales_report_columns

config = load_config()

#Set the environment
client = Square(
    environment=SquareEnvironment.SANDBOX,
    token= config['SQUARE']['api_key']
)

location = config['LOCATION']['main']


#view
def view_orders(start_date:str, end_date:str):
    order_entries = client.orders.search(
        location_ids=[location],
        # limit=2, #comment
        query={
            "filter": {
                "date_time_filter": {
                    "created_at": {
                        "start_at": start_date,
                        "end_at": end_date
                    }
                }
            },
            'sort':
            {
                'sort_field': 'CREATED_AT',
                'sort_order': 'DESC'
            }
        }
    )
    print(order_entries)
def search_order(order_id):
    return client.orders.get(order_id)

def count_files_in_folder(folder_path):
    """Counts the number of files in a given folder."""
    file_count = 0
    try:
        for entry in os.scandir(folder_path):
            if entry.is_file():
                file_count += 1
        return file_count
    except Exception as e:
        print(e)
def get_date_range(start_date, end_date):
    date_list = []
    current_date = start_date
    delta = timedelta(days=1)

    while current_date <= end_date:
        date_list.append(current_date.date())
        current_date += delta

    return date_list


# since the orders in the API are NOT created at different dates due to API constraints,
# the next approach is as follows:
#TODO:
# 1. Load EACH CSV file
# 2. Turn it into a dataFrame
# 3. For every Order ID in the DataFrame, get the order information to retrieve items. If, API calls are not convenient,
#   a solution is to save line items and its modifiers, along with the order for reference on a table.


def sales_report():
    start_date = datetime(2025, 8, 29)
    end_date = datetime(2025, 10, 15)

    date_list = get_date_range(start_date, end_date)
    # print(date_list)

    total_order_count = 0
    for date in date_list:
        date = date.strftime('%Y-%m-%d')
        # print(date) # 2025-08-29 to 2025-10-15

        df = pd.read_csv(filepath_or_buffer=f'../logs/inventory/{date}_log.CSV', header=None)
        filtered_df = set(filter(lambda x: x != '#NULL', list(df[6]))) #unique_id's without #NULLs
        # print(filtered_df)
        # total_order_count += len(filtered_df) #retrieve unique order_id's

        print(list(filtered_df))

        orders_in_a_day = client.orders.batch_get(
            location_id=location,
            order_ids=list(filtered_df)
        )


        item_list = item_list_count.copy()
        modifier_list = modifier_list_count.copy()

        print(item_list)
        print(modifier_list)
        #
        # # tally every product from every order and save it into item_list
        for order in orders_in_a_day.orders:
            for line_item in order.line_items:
                item_list[line_item.catalog_object_id] += int(line_item.quantity)
                if line_item.modifiers is not None:
                    for modifiers in line_item.modifiers:
                        modifier_list[modifiers.catalog_object_id] += int(modifiers.quantity)

        print(item_list)
        print(modifier_list)

        data = []
        grand_total = 0

        # for each product, retrieve the total tally and multiply it by its ppu
        for item_code, quantity in item_list.items():
            item = client.catalog.object.get(item_code).object

            name = item.item_variation_data.name
            quantity = quantity
            ppu = item.item_variation_data.price_money.amount
            total = quantity * ppu

            row = {
                'Name': name,
                'Quantity': quantity,
                'Price_per_unit': ppu,
                'Total': total
            }

            grand_total += total
            data.append(row)

        # do the same but for the ones that were modified
        for modifier_code, quantity in modifier_list.items():
            modifier = client.catalog.object.get(modifier_code)
            name = modifier.object.modifier_data.name
            quantity = quantity
            ppu = modifier.object.modifier_data.price_money.amount
            total = quantity * ppu
            row = {
                'Name': name,
                'Quantity': quantity,
                'Price_per_unit': ppu,
                'Total': total
            }

            grand_total += total
            data.append(row)

        last_row = {
            'Name': 'Grand_total',
            'Quantity': '',
            'Price_per_unit': '',
            'Total': grand_total
        }
        data.append(last_row)

        data_df = pd.DataFrame(data=data, columns=sales_report_columns)
        path= f'../logs/sales_report/{date}_report.CSV'
        data_df.to_csv(path_or_buf=path, mode='w', header=True, index=False)

if __name__ == '__main__':
    sales_report()