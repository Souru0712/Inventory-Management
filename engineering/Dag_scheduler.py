from datetime import datetime, timedelta
import uuid
import json
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from square.types.create_order_response import CreateOrderResponse
from square.client import Square
from square.environment import SquareEnvironment

from config.Config_loader import load_config
from engineering.square.Orders import increment_order_number
from engineering.square.Structures import ingredient_names, coffee_list, RECIPE_BOOK, modifier_milk_list, \
    modifier_syrup_list, modifier_shot_list, inventory_columns, item_list_count, modifier_list_count, sales_report_columns

config = load_config()
client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=config['SQUARE']['api_key']
)


# Task 1
def create_csv(**kwargs):
    dag_run = kwargs['dag_run']
    logical_date = dag_run.logical_date
    date =  logical_date.strftime('%Y-%m-%d')

    path= f'/opt/airflow/logs/inventory_with_dag/{date}_log.CSV'
    # path= f'../logs/inventory/{date}_log.CSV'

    df = pd.DataFrame(columns=inventory_columns)
    df.to_csv(path_or_buf=path, header=True, index=False)

# Task 2 is Alert_system.py
main_location = config['LOCATION']['main']
def create_draft_email(body:str):   # Email credentials
    msg = MIMEMultipart()
    msg['From'] = config['GOOGLE']['sender_email']
    msg['To'] = config['GOOGLE']['receiver_email']
    msg['Subject'] = 'Inventory Alert'
    msg.attach(MIMEText(body, 'plain'))

    return msg.as_string()

def create_alert(logical_date):

    #deprecated because the call includes IDs that do not exist
    # inventory = client.inventory.batch_get_counts(
    #     location_ids=[location],
    #     states=['IN_STOCK']
    # )

    ingredient_ids = [
        config['INGREDIENT']['espresso'],
        config['INGREDIENT']['whole_milk'],
        config['INGREDIENT']['oat_milk'],
        config['INGREDIENT']['almond_milk'],
        config['INGREDIENT']['soy_milk'],
        config['INGREDIENT']['4oz_cup'],
        config['INGREDIENT']['6oz_cup'],
        config['INGREDIENT']['12oz_cup'],
        config['INGREDIENT']['16oz_cup'],
        config['INGREDIENT']['vanilla_syrup'],
        config['INGREDIENT']['caramel_syrup'],
        config['INGREDIENT']['hazelnut_syrup'],
        config['INGREDIENT']['chocolate_syrup'],
        config['INGREDIENT']['seasonal_syrup']
    ]

    inventory = client.inventory.batch_get_counts(
        catalog_object_ids=ingredient_ids,
        location_ids=[main_location],
        states=['IN_STOCK']
    )

    low_inventory = {}
    reorder = []

    for item in inventory.items:
        item_data = client.catalog.object.get(object_id=item.catalog_object_id).object.item_variation_data
        if int(item.quantity) <= int(item_data.inventory_alert_threshold):
            low_inventory.update({item_data.name:item.quantity})
            reorder.append(item.catalog_object_id)

    if low_inventory != {}:

        body = f'Reminder:\n\n{logical_date}\n\nThese items are currently low count:\n\n'
        for ingredient_name, ingredient_quantity in low_inventory.items():
            body+=f'Item: {ingredient_name}\nQuantity: {ingredient_quantity}\n\n'
        body+='\nPlease reorder by (time)'
        message = create_draft_email(body=body)

        # Connect to server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config['GOOGLE']['sender_email'], config['GOOGLE']['app_password'])
        server.sendmail(config['GOOGLE']['sender_email'], config['GOOGLE']['receiver_email'], message)
        server.close()

    #return the list of ingredients that need to be reordered
    return reorder


        # TODO TWILIO
        #     twilio_bot = Client(config['TWILIO']["account_sid"], config['TWILIO']['auth_token'])
        #
        #     #LOGIC: some useful information for notifications could be units to go along. There could also be a prompt
        #     # that receives user input to direct them to a page to order for quick access or maybe vendor information
        #     # that help direct staff where to order and how much.
        #     message = twilio_bot.messages.create(
        #         from_=config['TWILIO']['from_phone'],
        #         body=f'Reminder: {item_data.name} is running low. There is currently {item.quantity} left in the inventory.',
        #         to=config['TWILIO']['to_phone']
        #     )

def stock_inventory(logical_date) -> dict:
    # -----------------------------------------------------------------------------------------------------------------
    # WARNING: For the sake of the simulator, NO DISTRIBUTOR IS INVOLVED.
    # restocking ingredients is immediate and requires no purchase
    # -----------------------------------------------------------------------------------------------------------------

    # TODO: Reminders can either notify you to order ingredients manually OR create restocking code that purchases from the distributor automatically

    restock = create_alert(logical_date)

    stock_ingredients = {}
    if restock != []:
        reorder_amounts = {
            config['INGREDIENT']['espresso']: 9072,

            config['INGREDIENT']['whole_milk']: 1024,
            config['INGREDIENT']['oat_milk']: 384,
            config['INGREDIENT']['almond_milk']: 384,
            config['INGREDIENT']['soy_milk']: 384,

            config['INGREDIENT']['4oz_cup']: 1000,
            config['INGREDIENT']['6oz_cup']: 1000,
            config['INGREDIENT']['12oz_cup']: 1000,
            config['INGREDIENT']['16oz_cup']: 1000,

            config['INGREDIENT']['vanilla_syrup']: 135,
            config['INGREDIENT']['caramel_syrup']: 135,
            config['INGREDIENT']['hazelnut_syrup']: 135,
            config['INGREDIENT']['chocolate_syrup']: 135,
            config['INGREDIENT']['seasonal_syrup']: 135
        }

        changes = []

        for ingredient in restock:
            adjustment = {
                "type": "ADJUSTMENT",
                "adjustment": {
                    'catalog_object_id': ingredient,
                    'from_state': 'NONE',
                    'to_state': 'IN_STOCK',
                    'location_id': config['LOCATION']['main'],
                    'quantity': str(reorder_amounts.get(ingredient)),
                    'occurred_at': datetime.now()
                }
            }
            changes.append(adjustment)
            stock_ingredients.update({ingredient: reorder_amounts.get(ingredient)})

        # send the request
        update = client.inventory.batch_create_changes(
            idempotency_key=str(uuid.uuid4()),
            changes=changes
        )

    return stock_ingredients

def stocking_log(**kwargs):
    dag_run = kwargs['dag_run']
    logical_date = dag_run.logical_date

    date =  logical_date.strftime('%Y-%m-%d')
    path= f'/opt/airflow/logs/inventory_with_dag/{date}_log.CSV'

    reorder_ingredients = stock_inventory(logical_date)

    try:
        if reorder_ingredients != {}:
            data = []
            for ingredient_code, amount in reorder_ingredients.items():
                if ingredient_names.get(ingredient_code) == 'espresso':
                    unit = '(g)'
                elif ingredient_names.get(ingredient_code).endswith('milk'):
                    unit = '(oz)'
                elif ingredient_names.get(ingredient_code).endswith('cup'):
                    unit = 'cup'
                else:
                    unit = 'pump'
                action = {
                    'Timestamp': logical_date,  # not accurate but at least it covers the date
                    'Reference_id': None,
                    'Action': 'Stocking',  # Following Task 3's action
                    'Ingredient': ingredient_names.get(ingredient_code),
                    'Amount': amount,
                    'Unit': unit,
                    'Order_id': None
                }
                data.append(action)
            df = pd.DataFrame(data=data, columns=inventory_columns)
            df.to_csv(path_or_buf=path, mode='a', header=False, index=False)
    except Exception as e:
        print(f"Error: {e}")
# ------------------------------------------------------------------------------------------------------------------------
class Reference_id:
    def __init__(self):
        last_order_number = client.orders.search(
        limit=1,
        location_ids=[main_location],
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
        self.count = last_order_number
    def increment(self):
        self.count += 1
        return self.count
def increment_reference_id(reference_id: Reference_id):
    current_order_number = reference_id.increment()

    if current_order_number < 10:
        current_order_id = f'#00000{current_order_number}'
    elif current_order_number < 100:
        current_order_id = f'#0000{current_order_number}'
    elif current_order_number < 1000:
        current_order_id = f'#000{current_order_number}'
    elif current_order_number < 10000:
        current_order_id = f'#00{current_order_number}'
    elif current_order_number < 100000:
        current_order_id = f'#0{current_order_number}'
    else:
        current_order_id = f'#{current_order_number}'

    return current_order_id

def create_random_order():
    total_drink = np.random.randint(1, 3)
    line_items = []
    total_ingredients = None
    ingredients_per_drink = []
    coffee_list_copy = coffee_list.copy()

    for drink in range(total_drink):
        code = np.random.choice(coffee_list_copy)
        quantity = np.random.randint(1, 2)  # order with either 1 drink or a total of 3 drinks

        for variation in range(quantity):
            # reset modifiers
            ingredients = RECIPE_BOOK.get(code).copy()

            dairy_choice = None
            syrup_choice = None
            shot_choice = None

            # Logic: check if the probability is triggered. If so, choose a dairy choice (can be regular milk) and get the ingredient id
            # check if the drink requires milk. If we picked whole milk then we should do nothing, otherwise, replace the milk.
            # If the drink does not need any milk, then by default, the drink should contain a little bit since they did modify it.

            is_milk_modified = round(np.random.random(), 2)
            if is_milk_modified <= 0.40:
                dairy_choice = np.random.choice(list(modifier_milk_list.keys()))
                dairy_ingredient = modifier_milk_list.get(dairy_choice)
                if dairy_ingredient != config['INGREDIENT']['whole_milk'] and config['INGREDIENT'][
                    'whole_milk'] in ingredients:
                    amount = ingredients.get(config['INGREDIENT']['whole_milk'])
                    ingredients.pop(config['INGREDIENT']['whole_milk'])
                    ingredients.update({dairy_ingredient: amount})
                elif config['INGREDIENT']['whole_milk'] not in ingredients:
                    ingredients.update({dairy_ingredient: 2})  # add any milk to a drink that may not include milk

            # Logic: check the probability again. if chocolate is chosen, then we need to see if the drink is a
            # mocha (contains chocolate milk). If so, then we should add more pumps for more chocolate flavor
            # Otherwise, we only add pumps if the drink does not require pumps by default (to avoid mixing another flavor
            # with chocolate)
            is_syrup_modified = round(np.random.random(), 2)
            if is_syrup_modified <= 0.30:
                syrup_choice = np.random.choice(list(modifier_syrup_list.keys()))
                syrup_ingredient = modifier_syrup_list.get(syrup_choice)
                if syrup_ingredient == config['INGREDIENT']['chocolate_syrup'] and config['INGREDIENT'][
                    'chocolate_syrup'] in ingredients:
                    amount = ingredients.get(syrup_ingredient) + 3
                    ingredients.update({syrup_ingredient: amount})
                elif config['INGREDIENT']['chocolate_syrup'] not in ingredients:
                    ingredients.update({syrup_ingredient: 3})  # default extra pumps

            # Logic: the only thing to look for in the extra shots is tracking extra depletion of espresso grams
            # so we only need to update the amount
            is_shot_modified = round(np.random.random(), 2)
            if is_shot_modified <= 0.15:
                shot_choice = np.random.choice(list(modifier_shot_list.keys()))
                shot_ingredient = modifier_shot_list.get(shot_choice)
                amount = ingredients.get(shot_ingredient)
                if shot_choice == config['MODIFIER']['extra_single_modification']:
                    amount += 9
                else:
                    amount += 18
                ingredients.update({shot_ingredient: amount})

            # TODO for the create_order call
            modifiers = []
            # check if probability was triggered and add it to the client call
            if dairy_choice is not None:
                modifiers.append({'catalog_object_id': dairy_choice})
            if syrup_choice is not None:
                modifiers.append({'catalog_object_id': syrup_choice})
            if shot_choice is not None:
                modifiers.append({'catalog_object_id': shot_choice})

            # create dict() for the line_item
            item = {
                "catalog_object_id": code,
                "quantity": "1",
                "modifiers": modifiers
            }

            # logic: check if the line_items has repetitive drink (including modifications).
            # If true, increase the count by 1. Else, we append it to the line_items
            is_incremented = False
            for made in line_items:
                if item.get("catalog_object_id") == made.get("catalog_object_id") and item.get("modifiers") == made.get(
                        "modifiers"):
                    made.update({"quantity": str(int(made.get("quantity")) + 1)})
                    is_incremented = True
                    break

            if not is_incremented:
                line_items.append(item)

            # TODO for the inventory management
            ingredients_per_drink.append(ingredients)

            if total_ingredients is None:
                total_ingredients = ingredients.copy()
            else:
                for ingredient_code in ingredients:
                    total_ingredients.update(
                        {ingredient_code: total_ingredients.get(ingredient_code, 0) + ingredients.get(ingredient_code)})
                    # set to 0 if the value does not exist and append with the current ingredient

            # print(f'line_items: {line_items}')
            # print()

    return (line_items, ingredients_per_drink, total_ingredients)
def create_random_hours(logical_date) -> list:

    hours = np.arange(8, 20)
    weights = [1.5, 1.5, 1.6, 1.2, 0.7, 0.6, 0.4, 0.5, 0.4, 0.8, 0.9, 1.0]
    weights = np.array(weights) / np.sum(weights)

    n_orders = 100
    chosen_hours = np.random.choice(hours, size=n_orders, p=weights)

    timestamps = []
    for h in chosen_hours:
        minute = np.random.randint(0, 60)
        # ts = dag_run.logical_date.replace(hour=h, minute=minute, second=0)
        ts = logical_date.replace(hour=h, minute=minute, second=0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        timestamps.append(ts)  # append Square-acceptable timestamps

    timestamps = sorted(timestamps)

    return timestamps


def create_receipt(all_receipts: list, reference_id: Reference_id, line_items: list) -> CreateOrderResponse:
    # send the request
    receipt = client.orders.create(
        idempotency_key=str(uuid.uuid4()),
        order={
            "reference_id": increment_reference_id(reference_id),
            "location_id": main_location,
            "line_items": line_items,
        }
        # for filtering created_at later (default to hour=0, minute=0, second=0)
        # created_at=logical_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    )
    all_receipts.append(receipt)

    return all_receipts

def accumulate_deduction(batch_ingredients_per_drinks: list, ingredients_per_drink: list):
    for drink in ingredients_per_drink:
        for ingredient_code, amount in drink.items():
            adjustment = {
                "type": "ADJUSTMENT",
                "adjustment": {
                    'catalog_object_id': ingredient_code,
                    'from_state': 'IN_STOCK',
                    'to_state': 'SOLD',
                    'location_id': main_location,
                    'quantity': str(amount),
                    'occurred_at': datetime.now()
                }
            }
        batch_ingredients_per_drinks.append(adjustment)

    return batch_ingredients_per_drinks

def complete_order(all_receipts:list):
    for receipt in all_receipts:
        order_id = receipt.order.id
        client.payments.create(
            source_id="cnon:card-nonce-ok", #for completing transactions in sandbox
            order_id=order_id,
            idempotency_key=str(uuid.uuid4()),
            location_id=config['LOCATION']['main'],
            amount_money=client.orders.get(order_id=order_id).order.total_money,
            autocomplete=True
        )

def deduct_inventory(batch_ingredients_per_drinks: list):
    # send the request (WARNING: changes array has a 100 limit for API call)

    #logic:
    # 1. floor division for-loop 2D array
    # 2. modulo request for the remainder

    limit = 100

    for i in range(len(batch_ingredients_per_drinks), limit): #limit of 100 elements in the changes field
        micro_batch = batch_ingredients_per_drinks[i:i+limit] #slicing also avoids index out of bounds error

        update = client.inventory.batch_create_changes(
            idempotency_key=str(uuid.uuid4()),
            changes=micro_batch
        )

def deduction_log(all_receipts: list, all_total_ingredients: list, timestamps: list, path: str):


    data = [] #for batch saving into CSV

    receipt_counter=0
    for total_ingredients in all_total_ingredients:
        for ingredient_code, amount in total_ingredients.items():
            if ingredient_names.get(ingredient_code) == 'espresso':
                unit = '(g)'
            elif ingredient_names.get(ingredient_code).endswith('milk'):
                unit = '(oz)'
            elif ingredient_names.get(ingredient_code).endswith('cup'):
                unit = 'cup'
            else:
                unit = 'pump'
            action = {
                'Timestamp': timestamps[receipt_counter],  # est_time
                'Reference_id': all_receipts[receipt_counter].order.reference_id,
                'Action': 'Deduct',
                'Ingredient': ingredient_names.get(ingredient_code),
                'Amount': amount,
                'Unit': unit,
                'Order_id': all_receipts[receipt_counter].order.id
            }
            data.append(action)

        receipt_counter += 1    #move to the next order

    df = pd.DataFrame(data=data, columns=inventory_columns)
    df.to_csv(path_or_buf=path, mode='a', header=False, index=False)


def simulate_business_day(**kwargs):
    # since dags call every task by the date,
    # We need to create a reference_id call for every date

    #logic:
    # 1. Call the API ONCE to fetch latest reference_id and save it into a static-like variable
    # 2. Every time an order is created the static variable will increment by one
    # 3. Create batch jobs to make processing for efficient.
    #       - make sure the workflow works with sufficient testing


    dag_run = kwargs['dag_run']
    logical_date = dag_run.logical_date

    date =  logical_date.strftime('%Y-%m-%d')
    path= f'/opt/airflow/logs/inventory_with_dag/{date}_log.CSV'

    np.random.seed(int(logical_date.strftime("%Y%m%d"))) #CRUCIAL: refreshes randomizer object so every logical_date has
                                                            # its own randomized order

    reference_id = Reference_id()
    all_receipts = []
    batch_ingredients_per_drinks = []
    all_total_ingredients = []

    for i in range(100): #100 orders
        # order workflow
        (line_items, ingredients_per_drink, total_ingredients) = create_random_order()
        all_receipts = create_receipt(all_receipts, reference_id, line_items) #append CreateOrderResponse
        batch_ingredients_per_drinks = accumulate_deduction(batch_ingredients_per_drinks, ingredients_per_drink) #append deduction
        all_total_ingredients.append(total_ingredients)

    timestamps = create_random_hours(logical_date)  # 100 ts
    complete_order(all_receipts) #bacth completion
    deduct_inventory(batch_ingredients_per_drinks) #batch deduction after the day is finished (inventory should be able to hold)
    deduction_log(all_receipts, all_total_ingredients, timestamps, path) #batch logging
def sales_report(**kwargs):
    dag_run = kwargs['dag_run']
    logical_date = dag_run.logical_date
    date_name = logical_date.strftime('%Y-%m-%d')

    df = pd.read_csv(f'/opt/airflow/logs/inventory_with_dag/{date_name}_log.CSV', header=0)
    filtered_df = set(filter(lambda x: x != '#NULL', list(df['Order_id']))) #unique_id's and filtering out NULL orders

    orders_in_a_day = client.orders.batch_get(
        location_id=main_location,
        order_ids=list(filtered_df)
    )

    item_list = item_list_count.copy()
    modifier_list = modifier_list_count.copy()

    # tally every product and any modifiers from every order and save it into the corresponding list
    for order in orders_in_a_day.orders:
        for line_item in order.line_items:
            item_list[line_item.catalog_object_id] += int(line_item.quantity)
            if line_item.modifiers is not None:
                for modifiers in line_item.modifiers:
                    modifier_list[modifiers.catalog_object_id] += int(modifiers.quantity)

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

    #save batch into CSV for the given date
    data_df = pd.DataFrame(data=data, columns=sales_report_columns)
    path= f'/opt/airflow/logs/sales_report_with_dag/{date_name}_report.CSV'
    data_df.to_csv(path_or_buf=path, mode='w', header=True, index=False)
