from datetime import datetime, timedelta
import uuid
import json
import pandas as pd
import numpy as np
import pendulum

from square.types.create_order_response import CreateOrderResponse
from square.client import Square
from square.environment import SquareEnvironment

from config.Config_loader import load_config
from engineering.square.Orders import increment_order_number
from engineering.square.Structures import ingredient_names, coffee_list, RECIPE_BOOK, modifier_milk_list, \
    modifier_syrup_list, modifier_shot_list, all_modifiers, simulator_columns, milk_ingredients, syrup_ingredients, shot_ingredients

config = load_config()
client = Square(
    environment=SquareEnvironment.SANDBOX,
    token= config['SQUARE']['api_key']
)

class MockDagRun:
    def __init__(self, logical_date):
        self.logical_date = logical_date
class Reference_id:
    def __init__(self):
        self.count = 0
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
    # else:
    #     print("Congratulations! You are the ten thousandth customer! ")
    #     current_order_number = 0
    #     current_order_id = f'#000{current_order_number}'

    return current_order_id
def get_date_range(start_date, end_date):
    date_list = []
    current_date = start_date
    delta = timedelta(days=1)

    while current_date <= end_date:
        date_list.append(current_date.date())
        current_date += delta

    return date_list

def create_csv(path:str, **kwargs):
    # dag_run = kwargs['dag_run']
    # logical_date = dag_run.logical_date
    # date =  logical_date.strftime('%Y-%m-%d')

    # path= f'/opt/airflow/logs/inventory/{date}_log.CSV'
    # path= f'../logs/inventory/{date}_log.CSV'

    df = pd.DataFrame(columns=simulator_columns)
    df.to_csv(path_or_buf=path, header=True, index=False)

    return path
def create_random_order():
    total_drink = np.random.randint(1,3)
    line_items = []
    total_ingredients = None
    ingredients_per_drink = []
    coffee_list_copy = coffee_list.copy()

    for drink in range(total_drink):
        code = np.random.choice(coffee_list_copy)
        quantity = np.random.randint(1,2) #order with either 1 drink or a total of 3 drinks

        for variation in range(quantity):
            #reset modifiers
            ingredients = RECIPE_BOOK.get(code).copy()

            dairy_choice = None
            syrup_choice = None
            shot_choice = None

            #Logic: check if the probability is triggered. If so, choose a dairy choice (can be regular milk) and get the ingredient id
            # check if the drink requires milk. If we picked whole milk then we should do nothing, otherwise, replace the milk.
            # If the drink does not need any milk, then by default, the drink should contain a little bit since they did modify it.

            is_milk_modified = round(np.random.random(), 2)
            if is_milk_modified <= 0.40:
                dairy_choice = np.random.choice(list(modifier_milk_list.keys()))
                dairy_ingredient = modifier_milk_list.get(dairy_choice)
                if dairy_ingredient != config['INGREDIENT']['whole_milk'] and config['INGREDIENT']['whole_milk'] in ingredients:
                    amount = ingredients.get(config['INGREDIENT']['whole_milk'])
                    ingredients.pop(config['INGREDIENT']['whole_milk'])
                    ingredients.update({dairy_ingredient: amount})
                elif config['INGREDIENT']['whole_milk'] not in ingredients:
                    ingredients.update({dairy_ingredient: 2}) #add any milk to a drink that may not include milk

            #Logic: check the probability again. if chocolate is chosen, then we need to see if the drink is a
            # mocha (contains chocolate milk). If so, then we should add more pumps for more chocolate flavor
            # Otherwise, we only add pumps if the drink does not require pumps by default (to avoid mixing another flavor
            # with chocolate)
            is_syrup_modified = round(np.random.random(), 2)
            if is_syrup_modified <= 0.30:
                syrup_choice = np.random.choice(list(modifier_syrup_list.keys()))
                syrup_ingredient = modifier_syrup_list.get(syrup_choice)
                if syrup_ingredient == config['INGREDIENT']['chocolate_syrup'] and config['INGREDIENT']['chocolate_syrup'] in ingredients:
                    amount = ingredients.get(syrup_ingredient) + 3
                    ingredients.update({syrup_ingredient: amount})
                elif config['INGREDIENT']['chocolate_syrup'] not in ingredients:
                    ingredients.update({syrup_ingredient: 3}) #default extra pumps

            #Logic: the only thing to look for in the extra shots is tracking extra depletion of espresso grams
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
                ingredients.update({shot_ingredient:amount})

            #TODO for the create_order call
            modifiers = []
            #check if probability was triggered and add it to the client call
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

            #logic: check if the line_items has repetitive drink (including modifications).
            # If true, increase the count by 1. Else, we append it to the line_items
            is_incremented = False
            for made in line_items:
                if item.get("catalog_object_id") == made.get("catalog_object_id") and item.get("modifiers") == made.get("modifiers"):
                    made.update({"quantity":str(int(made.get("quantity"))+1)})
                    is_incremented = True
                    break

            if not is_incremented:
                line_items.append(item)

            #TODO for the inventory management
            ingredients_per_drink.append(ingredients)

            if total_ingredients is None:
                total_ingredients = ingredients.copy()
            else:
                for ingredient_code in ingredients:
                    total_ingredients.update({ingredient_code: total_ingredients.get(ingredient_code, 0) + ingredients.get(ingredient_code)})
                    #set to 0 if the value does not exist and append with the current ingredient

            # print(f'line_items: {line_items}')
            # print()

    return (line_items, ingredients_per_drink, total_ingredients)
def create_random_hours(logical_date, **kwargs) -> list:
    # dag_run = kwargs['dag_run']
    # logical_date = dag_run.logical_date
    hours = np.arange(8, 20)
    weights = [1.5, 1.5, 1.6, 1.2, 0.7, 0.6, 0.4, 0.5, 0.4, 0.8, 0.9, 1.0]
    weights = np.array(weights) / np.sum(weights)

    n_orders = 1000
    chosen_hours = np.random.choice(hours, size=n_orders, p=weights)

    timestamps = []
    for h in chosen_hours:
        minute = np.random.randint(0, 60)
        # ts = dag_run.logical_date.replace(hour=h, minute=minute, second=0)
        ts = logical_date.replace(hour=h, minute=minute, second=0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        timestamps.append(ts) #append Square-acceptable timestamps

    timestamps = sorted(timestamps)

    return timestamps

def deduct_inventory(ingredients_per_drink:list):
    changes = []
    for drink in ingredients_per_drink:
        for ingredient_code, amount in drink.items():
            adjustment = {
                "type": "ADJUSTMENT",
                "adjustment": {
                    'catalog_object_id': ingredient_code,
                    'from_state': 'IN_STOCK',
                    'to_state': 'SOLD',
                    'location_id': config['LOCATION']['main'],
                    'quantity': str(amount),
                    'occurred_at': datetime.now()
                }
            }
        changes.append(adjustment)

    #send the request
    update = client.inventory.batch_create_changes(
        idempotency_key=str(uuid.uuid4()),
        changes=changes
    )

def deduction_log(receipt: CreateOrderResponse, total_ingredients: dict, ts:str, path:str):

    data = []
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
            'Timestamp': ts, #est_time
            'Location_id': receipt.order.location_id,
            'Location_name': "Nyanya's Brooklyn" if receipt.order.location_id == config['LOCATION']['main'] else "Nyanya's Queens",
            'Reference_id': receipt.order.reference_id,
            'Action': 'Deduct',
            'Ingredient': ingredient_names.get(ingredient_code),
            'Amount': amount,
            'Unit': unit,
            'Order_id': 'Sample'
        }
        data.append(action)
    df = pd.DataFrame(data=data, columns=simulator_columns)
    df.to_csv(path_or_buf=path, mode='a', header=False, index=False)

def simulate_business_day(reference_id: Reference_id, path:str, **kwargs):
    dag_run = kwargs['dag_run']
    logical_date = dag_run.logical_date
    timestamps = create_random_hours(logical_date) #1000 ts or 1000 orders across 2 locations


    for ts in timestamps:
        random_location = np.random.choice([config['LOCATION']['main'], 'L7P7YENXAAKPY'])
        #Create sample CSV's LOGIC: NO API CALLS INCLUDED
        (line_items, ingredients_per_drink, total_ingredients) = create_random_order()
        receipt = CreateOrderResponse(
            idempotency_key=str(uuid.uuid4()),
            order={
            "reference_id": increment_reference_id(reference_id),
            "location_id": random_location,
            "line_items": line_items
            }
        )
        deduction_log(receipt, total_ingredients, ts, path)

if __name__ == '__main__':
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12,31)

    date_list = get_date_range(start_date, end_date)
    path = f'../logs/inventory/inventory_log.CSV'
    create_csv(path)
    reference_id = Reference_id()

    for date in date_list:
        print(date)
        dt = datetime.strptime(str(date), '%Y-%m-%d')
        mock_dag_run_instance = MockDagRun(logical_date=dt)
        mock_kwargs = {'dag_run': mock_dag_run_instance}
        simulate_business_day(reference_id, path, **mock_kwargs)

    df = pd.read_csv(path)
    print(len(df))