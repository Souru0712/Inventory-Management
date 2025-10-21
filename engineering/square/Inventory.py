from datetime import datetime
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

def view_inventory_at_location(location=location):
    response = client.inventory.batch_get_counts(
        location_ids=[location]
    )

    for item in response.items:
        info = client.catalog.object.get(object_id=item.catalog_object_id)
        print(f'name: {info.object.item_variation_data.name} id:{item.catalog_object_id}, location:{item.location_id}, quantity:{item.quantity}')
# NOTE: type PHYSICAL COUNT sets while ADJUSTMENT aggregates
#group requests based on same quantity
def create_inventory():
    #espresso
    try:
        client.inventory.batch_create_changes(
            idempotency_key=str(uuid.uuid4()),
            changes=[
                {
                    #espresso
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['espresso'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '13608',
                        "occurred_at": datetime.now()
                    }
                },

                #cups
                {
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['4oz_cup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '2000',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['6oz_cup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '2000',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['12oz_cup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '2000',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['16oz_cup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '2000',
                        "occurred_at": datetime.now()
                    }
                },

                #syrup
                {
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['vanilla_syrup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '405',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['caramel_syrup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '405',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['hazelnut_syrup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '405',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['chocolate_syrup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '405',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['seasonal_syrup'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '405',
                        "occurred_at": datetime.now()
                    }
                },

                #whole milk
                {
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['whole_milk'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '1536',
                        "occurred_at": datetime.now()
                    }
                },


                #non-dairy
                {
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['oat_milk'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '768',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['almond_milk'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '768',
                        "occurred_at": datetime.now()
                    }
                },{
                    "type": "PHYSICAL_COUNT",
                    "physical_count": {
                        "catalog_object_id": config['INGREDIENT']['soy_milk'],
                        "state": "IN_STOCK",
                        "location_id": config['LOCATION']['main'],
                        "quantity": '768',
                        "occurred_at": datetime.now()
                    }
                }
            ]
        )
    except Exception as e:
        print(f'Inventory set default failed: {e}')

if __name__ == '__main__':
    create_inventory()
    view_inventory_at_location()