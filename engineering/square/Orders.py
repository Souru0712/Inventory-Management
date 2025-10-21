import uuid
from square.client import Square
from square.environment import SquareEnvironment

from config.Config_loader import load_config

config = load_config()

#Set the environment
client = Square(
    environment=SquareEnvironment.SANDBOX,
    token= config['SQUARE']['api_key']
)

location = config['LOCATION']['main']

#WARNING: dict() is mutable so references will change the same object
# Solution: create a copy of the ingredients so that every time the recipe book is fetched, the original recipe is called

def retrieve_all_items():
    items = client.catalog.list(types='ITEM_VARIATION')
    for item in items:
        if item.item_variation_data.track_inventory==None:
            # print(item.item_variation_data.name)
            print(f'\'{item.id}\',')
        # print(item.item_data.variations.)
def view_modifier():
    option = client.catalog.list(types='MODIFIER_LIST')
    for choice in option:
        print(choice)
        for modifier in choice.modifier_list_data.modifiers:
            print(modifier)
            print(f'\'{modifier.id}\',')
def create_first_order():
    receipt = client.orders.create(
        idempotency_key=str(uuid.uuid4()),
        order={
            "reference_id": "#0001",
            "location_id": config['LOCATION']['main'],
            'line_items': [{
                "catalog_object_id": 'LZQVGFNDPCEUM2XQNKL2HRS5', #hot_espresso
                "quantity": "1"
            }]
        }
    )
    return receipt

def return_orders():
    order_entries = client.orders.search(
        location_ids=[location],
        # limit=2, #comment
        query={'sort':
            {
                'sort_field':'CREATED_AT',
                'sort_order':'DESC'
            }
        }
    )
    print(order_entries)
    try:
        for order in order_entries.orders:
            print(f'order_id={order.id}, '
                f'order_number={order.reference_id}, '
                f'order={[(item.variation_name, item.quantity, [modifier.name for modifier in item.modifiers], item.total_money.amount) if item.modifiers is not None else (item.variation_name, item.quantity, None, item.total_money.amount) for item in order.line_items]}, '
                f'total=${order.net_amounts.total_money.amount / 100}, '
                f'state={order.state}')
    except Exception as e:
        print(f'order_number {order.reference_id} skipped. {e}.')
def increment_order_number():
    # Increment order number based off the latest order
    last_order_number = client.orders.search(
        limit=1,
        location_ids=[location],
        query={
            "filter": {
                "state_filter": {
                    "states": [
                        "OPEN",
                        "COMPLETED"
                    ]
                }
            },
            "sort": {
                "sort_field": "CREATED_AT",
                "sort_order": "DESC"
            }
        }
    ).orders[0].reference_id
    last_order_number = int(last_order_number[1:])
    current_order_number = last_order_number + 1
    if current_order_number < 10:
        current_order_id = f'#000{current_order_number}'
    elif current_order_number < 100:
        current_order_id = f'#00{current_order_number}'
    elif current_order_number < 1000:
        current_order_id = f'#0{current_order_number}'
    elif current_order_number < 10000:
        current_order_id = f'#{current_order_number}'
    else:
        print("Congratulations! You are the ten thousandth customer! ")
        current_order_number = 0
        current_order_id = f'#000{current_order_number}'


    return current_order_id


# def test(item_list_count):
#     data = []
#     grand_total = 0
#     for item_code, quantity in item_list_count.items():
#         item = client.catalog.object.get(item_code).object
#         name = item.item_variation_data.name
#         quantity = quantity
#         ppu = item.item_variation_data.price_money.amount
#         total = quantity*ppu
#         row = {
#             'Name': name,
#             'Quantity': quantity,
#             'Price_per_unit': ppu,
#             'Total': total,
#         }
#         data.append(row)
#         grand_total += total
#
#     last_row = {
#         'Name': 'Grand_total',
#         'Quantity': '',
#         'Price_per_unit': '',
#         'Total': grand_total,
#     }
#     data.append(last_row)
#
#     df = pd.DataFrame(data=data, columns=columns)
#     print(df)

# print(client.orders.search(location_ids=[location]))