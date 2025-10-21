import uuid
from square.client import Square
from square.environment import SquareEnvironment
from config.Config_loader import load_config

config = load_config()
location = config['LOCATION']['main']

#Set the environment
client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=config['SQUARE']['api_key']
)

# view all created objects and their IDs, then their variations
def view_catalog():
    for object in client.catalog.list():
        print(object)
        print(object.id)
def view_catalog_variations():
    for object in client.catalog.list(types='ITEM_VARIATION'):
        print(f'{object.item_variation_data.name}: {object.id}')

def view_inventory():
    item_variation_ids = []

    item_search = client.catalog.list(types='ITEM_VARIATION')
    for item in item_search:
        print(f'{item.item_variation_data.name}: {item.id}')
        item_variation_ids.append(item.id)

    inventory = client.inventory.batch_get_counts(
        location_ids=[location],
        states=['IN_STOCK']
    )

    for inventory_item in inventory:
        if inventory_item.catalog_object_id in item_variation_ids:
            print(f'safe: {inventory_item.catalog_object_id}')


    for inventory_item in inventory:
        if inventory_item.catalog_object_id not in item_variation_ids:
            print(f'culprit: {inventory_item.catalog_object_id}')
            client.catalog.object.get(object_id=inventory_item.catalog_object_id)

# Send the request for modifiers(milk, syrups, shots), products, and ingredients for stocking
def create_catalog_modifiers():
    result = client.catalog.batch_upsert(
        idempotency_key=str(uuid.uuid4()),
        batches=[
            {
                'objects': [
                    {
                        "type": "MODIFIER_LIST",
                        "id": '#Milk_list',
                        "present_at_location_ids": [config['LOCATION']['main']],
                        "modifier_list_data": {
                            "name": "milk_list",
                            "modifiers": [
                                {
                                    "type": "MODIFIER",
                                    "id": "#Whole Milk",
                                    "modifier_data": {
                                        "name": "regular_modification",
                                        "price_money": {"amount": 0, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Oat Milk",
                                    "modifier_data": {
                                        "name": "oat_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Almond Milk",
                                    "modifier_data": {
                                        "name": "almond_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Soy Milk",
                                    "modifier_data": {
                                        "name": "soy_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Skim Milk",
                                    "modifier_data": {
                                        "name": "skim_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Cream",
                                    "modifier_data": {
                                        "name": "cream_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Heavy Milk",
                                    "modifier_data": {
                                        "name": "heavy_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                }
                            ]
                        }
                    }, {
                        "type": "MODIFIER_LIST",
                        "id": '#Syrup_list',
                        "present_at_location_ids": [config['LOCATION']['main']],
                        "modifier_list_data": {
                            "name": "syrup_list",
                            "modifiers": [
                                {
                                    "type": "MODIFIER",
                                    "id": "#Vanilla Syrup",
                                    "modifier_data": {
                                        "name": "vanilla_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Caramel Syrup",
                                    "modifier_data": {
                                        "name": "caramel_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Hazelnut Syrup",
                                    "modifier_data": {
                                        "name": "hazelnut_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Chocolate Syrup",
                                    "modifier_data": {
                                        "name": "chocolate_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Seasonal Syrup",
                                    "modifier_data": {
                                        "name": "seasonal_modification",
                                        "price_money": {"amount": 50, "currency": "USD"}
                                    }
                                }
                            ]
                        }
                    }, {
                        "type": "MODIFIER_LIST",
                        "id": "#Extra_shot_list",
                        "present_at_location_ids": [config['LOCATION']['main']],
                        "modifier_list_data": {
                            "name": "extra_shot_list",
                            "modifiers": [
                                {
                                    "type": "MODIFIER",
                                    "id": "#Extra Single Shot",
                                    "modifier_data": {
                                        "name": "extra_single_modification",
                                        "price_money": {"amount": 150, "currency": "USD"}
                                    }
                                },
                                {
                                    "type": "MODIFIER",
                                    "id": "#Extra Double Shot",
                                    "modifier_data": {
                                        "name": "extra_double_modification",
                                        "price_money": {"amount": 275, "currency": "USD"}
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    )
    for object in result.objects:
        config['MODIFIER'][f'{object.modifier_list_data.name}'] = object.id
        for modifier in object.modifier_list_data.modifiers:
            config['MODIFIER'][f'{modifier.modifier_data.name}'] = modifier.id

    with open('../../config/config.ini', 'w') as configfile:
        config.write(configfile)
def create_catalog_items():
    coffee_list = {
        'Espresso': ['Concentrated shot of coffee', 175, 250],   # optional ice
        'Doppio': ['Double the strength', 325, 400],   # optional ice
        'Macchiato': ['Espresso with a dollop of foam', 200, 275],  # optional ice
        'Doppio macchiato': ['Double espresso with foam', 350, 425],   # optional ice
        'Cortado': ['Equal parts espresso and steamed milk', 350, 425],  # optional ice

        'Cappuccino': ['Equal parts espresso, steamed milk, foam', 375, 450],  # optional ice
        'Flat white': ['Espresso + steamed milk (less foam)', 375, 575],
        'Pour over': ['Columbian blend with complementary milks', 200, 275],  # optional ice

        'Americano': ['Espresso + hot water', 350, 550],
        'Latte': ['Espresso + steamed milk + light foam', 450, 525],
        'Mocha': ['Latte with chocolate', 500, 575],
        'Red Eye': ['Espresso shot on pour over', 375, 450],  # optional ice
        'Black Eye': ['Double shot on pour over', 525, 600],  # optional ice
        'Matcha Latte': ['Ceremonial Green Tea powder + milk', 500, 575],   # optional ice
        'Hojicha Latte': ['Roasted Green Tea powder with milk', 375, 450],   # optional ice
        'Chai Latte': ['Spiced Black Tea', 450, 525]  # optional ice
    }
    # Send the request for items(every coffee drink)
    for item, attribute in coffee_list.items():
        result = client.catalog.batch_upsert(
            idempotency_key=str(uuid.uuid4()),
            batches=[
                {
                    'objects': [
                        {
                            "type": "ITEM",
                            "id": f'#{item}',
                            "present_at_location_ids": [config['LOCATION']['main']],
                            "item_data": {
                                "name": item,
                                "description": attribute[0],
                                "variations": [
                                    {
                                        "type": "ITEM_VARIATION",
                                        "id": f'#Hot {item}',
                                        "item_variation_data": {
                                            "name": f"hot_{item}",
                                            "pricing_type": "FIXED_PRICING",
                                            "price_money": {"amount": attribute[1], "currency": "USD"}
                                        }
                                    },
                                    {
                                        "type": "ITEM_VARIATION",
                                        "id": f'#Iced {item}',
                                        "item_variation_data": {
                                            "name": f"iced_{item}",
                                            "pricing_type": "FIXED_PRICING",
                                            "price_money": {"amount": attribute[2], "currency": "USD"}
                                        }
                                    }
                                ],
                                #include the modifiers
                                "modifier_list_info": [
                                    {"modifier_list_id": config['MODIFIER']['milk_list'], "enabled": True},
                                    {"modifier_list_id": config['MODIFIER']['syrup_list'], "enabled": True},
                                    {"modifier_list_id": config['MODIFIER']['extra_shot_list'], "enabled": True}
                                ]
                            }
                        }
                    ]
                }
            ]
        )
        for object in result.objects:
            for variation in object.item_data.variations:
                config['COFFEE'][f'{variation.item_variation_data.name}'] = variation.id

        with open('../../config/config.ini', 'w') as configfile:
            config.write(configfile)
def create_catalog_ingredients():
    result = client.catalog.batch_upsert(
        idempotency_key=str(uuid.uuid4()),
        batches=[
            {
                'objects': [
                    {
                        "type": "ITEM",
                        "id": "#Coffee",
                        "present_at_location_ids": [config['LOCATION']['main']],
                        "item_data": {
                            "name": "Coffee",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Espresso",
                                    "item_variation_data": {
                                        "name": "espresso",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 3402
                                    }
                                }
                            ]
                        }
                    }, {
                        "type": "ITEM",
                        "id": "#Milks",
                        "present_at_location_ids": [config['LOCATION']['main']],
                        "item_data": {
                            "name": "Milks",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Whole milk",
                                    "item_variation_data": {
                                        "name": "whole_milk",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 512
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Oat Milk",
                                    "item_variation_data": {
                                        "name": "oat_milk",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 128
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Almond Milk",
                                    "item_variation_data": {
                                        "name": "almond_milk",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 128
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Soy Milk",
                                    "item_variation_data": {
                                        "name": "soy_milk",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 128
                                    }
                                }
                            ]
                        }
                    }, {
                        "type": "ITEM",
                        "id": "#Cups",
                        "present_at_location_ids": [config['LOCATION']['main']],
                        "item_data": {
                            "name": "Cups",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": "#4oz Cup",
                                    "item_variation_data": {
                                        "name": "4oz_cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 100
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#6oz Cup",
                                    "item_variation_data": {
                                        "name": "6oz_cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 250
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#12oz Cup",
                                    "item_variation_data": {
                                        "name": "12oz_cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 250
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#16oz Cup",
                                    "item_variation_data": {
                                        "name": "16oz_cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 250
                                    }
                                }
                            ]
                        }
                    }, {
                        "type": "ITEM",
                        "id": "#Syrups",
                        "present_at_location_ids": [config['LOCATION']['main']],
                        "item_data": {
                            "name": "Syrups",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Vanilla Syrup",
                                    "item_variation_data": {
                                        "name": "vanilla_syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 135
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Caramel Syrup",
                                    "item_variation_data": {
                                        "name": "caramel_syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 135
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Hazelnut Syrup",
                                    "item_variation_data": {
                                        "name": "hazelnut_syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 135
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Chocolate Syrup",
                                    "item_variation_data": {
                                        "name": "chocolate_syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 135
                                    }
                                }, {
                                    "type": "ITEM_VARIATION",
                                    "id": "#Seasonal Syrup",
                                    "item_variation_data": {
                                        "name": "seasonal_syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 135
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    )
    for object in result.objects:
        for variation in object.item_data.variations:
            config['INGREDIENT'][f'{variation.item_variation_data.name}'] = variation.id

    with open('../../config/config.ini', 'w') as configfile:
        config.write(configfile)

#modifying
# def update_milk_modifier():
#     result = client.catalog.batch_upsert(
#         idempotency_key=str(uuid.uuid4()),
#         batches=[
#             {
#                 'objects': [
#                     {
#                         "type": "MODIFIER_LIST",
#                         "id": config['MILK']['milk_list'],
#                         "version": 1755118562841,
#                         "modifier_list_data": {
#                             "name": "Milk Choices",
#                             "modifiers": [
#                                 {
#                                     "type": "MODIFIER",
#                                     "id": f'#Whole Milk',
#                                     "modifier_data": {
#                                         "name": "Whole Milk",
#                                         "price_money": {"amount": 0, "currency": "USD"}
#                                     }
#                                 },
#                                 {
#                                     "type": "MODIFIER",
#                                     "id": f'#Oat Milk',
#                                     "modifier_data": {
#                                         "name": "Oat Milk",
#                                         "price_money": {"amount": 75, "currency": "USD"}
#                                     }
#                                 },
#                                 {
#                                     "type": "MODIFIER",
#                                     "id": f'#Almond Milk',
#                                     "modifier_data": {
#                                         "name": "Almond Milk",
#                                         "price_money": {"amount": 75, "currency": "USD"}
#                                     }
#                                 },
#                                 {
#                                     "type": "MODIFIER",
#                                     "id": f'#Soy Milk',
#                                     "modifier_data": {
#                                         "name": "Soy Milk",
#                                         "price_money": {"amount": 75, "currency": "USD"}
#                                     }
#                                 },
#                                 {
#                                     "type": "MODIFIER",
#                                     "id": f'#Skim Milk',
#                                     "modifier_data": {
#                                         "name": "Skim Milk",
#                                         "price_money": {"amount": 25, "currency": "USD"}
#                                     }
#                                 },
#                                 {
#                                     "type": "MODIFIER",
#                                     "id": f'#Cream Milk',
#                                     "modifier_data": {
#                                         "name": "Half & Half",
#                                         "price_money": {"amount": 25, "currency": "USD"}
#                                     }
#                                 },
#                                 {
#                                     "type": "MODIFIER",
#                                     "id": f'#Heavy Milk',
#                                     "modifier_data": {
#                                         "name": "Heavy Milk",
#                                         "price_money": {"amount": 25, "currency": "USD"}
#                                     }
#                                 }
#                             ]
#                         }
#                     }
#                 ]
#             }
#         ]
#     )
def change_catalog_items():
    version = client.catalog.object.get("AOYXS6GAPKR7XVYXSXIPALQJ").object.version
    result = client.catalog.batch_upsert(
        idempotency_key=str(uuid.uuid4()),
        batches=[
            {
                'objects': [
                    {
                        "type": "ITEM",
                        "id": "AOYXS6GAPKR7XVYXSXIPALQJ",
                        "version": version,
                        "item_data": {
                            "name": "Coffee",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['espresso'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Espresso (g)",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 9072  # 4 bags
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "ITEM",
                        "id": "N34GMGDY7G6UHGWYKCA3UH4G",
                        "version": version,
                        "item_data": {
                            "name": "Milks",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['whole_milk'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Whole Milk (oz)",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 1024 #8 gallons
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['oat_milk'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Oat Milk (oz)",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 384
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['almond_milk'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Almond (oz)",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 384
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['soy_milk'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Soy Milk (oz)",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 384
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "ITEM",
                        "id": '5SMAKOWKPUHW3HEVORK4TP4B',
                        "version": version,
                        "item_data": {
                            "name": "Cup",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['4oz_cup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "4oz Cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 1000
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['6oz_cup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "6oz Cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 1000
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['12oz_cup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "12oz Cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 1000
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['16oz_cup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "16oz Cup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 1000
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "ITEM",
                        "id": 'ZYNNK7XGRGMIIW4T2F32PLSV',
                        "version": version,
                        "item_data": {
                            "name": "Syrup",
                            "variations": [
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['vanilla_syrup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Vanilla Syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 270
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['caramel_syrup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Caramel Syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 270
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['hazelnut_syrup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Hazelnut Syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 270
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['chocolate_syrup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Chocolate Syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 270
                                    }
                                },
                                {
                                    "type": "ITEM_VARIATION",
                                    "id": config['INGREDIENT']['seasonal_syrup'],
                                    "version": version,
                                    "item_variation_data": {
                                        "name": "Seasonal Syrup",
                                        "pricing_type": "FIXED_PRICING",
                                        "price_money": {"amount": 0, "currency": "USD"},
                                        "track_inventory": True,
                                        "inventory_alert_type": "LOW_QUANTITY",
                                        "inventory_alert_threshold": 270
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    )

#deletion
def delete_duplicates(id_list:list):
    client.catalog.batch_delete(
        object_ids=id_list
    )
def delete_all():
    id_list= []
    for object in client.catalog.list():
        id_list.append(object.id)
    delete_duplicates(id_list)
def create_items():
    try:
        delete_all()
        create_catalog_modifiers()
        create_catalog_items()
        create_catalog_ingredients()
        view_catalog()
    except Exception as e:
        print(f'item creations failed: {e}')

if __name__ == '__main__':
    # create_items()
    # print()
    # view_catalog()
    # view_catalog_variations()
    view_inventory()