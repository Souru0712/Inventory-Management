from config.Config_loader import load_config

config=load_config()

global RECIPE_BOOK
RECIPE_BOOK= {
    config['COFFEE']['hot_espresso']: {
            config['INGREDIENT']['espresso']: 9,
            config['INGREDIENT']['4oz_cup']: 1
    },
    config['COFFEE']['hot_doppio']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['4oz_cup']: 1
    },
    config['COFFEE']['hot_macchiato']: {
            config['INGREDIENT']['espresso']: 9,
            config['INGREDIENT']['4oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 1
    },
    config['COFFEE']['hot_doppio_macchiato']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['4oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 1
    },
    config['COFFEE']['hot_cortado']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['4oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 2
    },
    config['COFFEE']['hot_cappuccino']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['6oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 2
    },
    config['COFFEE']['hot_flat_white']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['6oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 3
    },
    config['COFFEE']['hot_pour_over']: {
            config['INGREDIENT']['espresso']: 11,
            config['INGREDIENT']['6oz_cup']: 1
    },
    config['COFFEE']['hot_americano']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['12oz_cup']: 1,
    },
    config['COFFEE']['hot_latte']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['12oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 8
    },
    config['COFFEE']['hot_mocha']:{
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['12oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 8,
            config['INGREDIENT']['chocolate_syrup']: 3,
    },
    config['COFFEE']['hot_red_eye']: {
            config['INGREDIENT']['espresso']: 27,
            config['INGREDIENT']['12oz_cup']: 1,
    },
    config['COFFEE']['hot_black_eye']: {
            config['INGREDIENT']['espresso']: 36,
            config['INGREDIENT']['12oz_cup']: 1,
    },
    # config['COFFEE']['hot_matcha_latte']: [
    #     {
    #         config['INGREDIENT']['espresso']: 18,
    #         config['INGREDIENT']['12oz_cup']: 1,
    #         config['INGREDIENT']['whole_milk']: 10
    #     }
    # ],
    # config['COFFEE']['hot_hojicha_latte']: [
    #     {
    #         config['INGREDIENT']['espresso']: 18,
    #         config['INGREDIENT']['12oz_cup']: 1,
    #         config['INGREDIENT']['whole_milk']: 10
    #     }
    # ],
    # config['COFFEE']['hot_chai_latte']: [
    #     {
    #         config['INGREDIENT']['espresso']: 18,
    #         config['INGREDIENT']['12oz_cup']: 1,
    #         config['INGREDIENT']['whole_milk']: 10
    #     }
    # ],

    config['COFFEE']['iced_espresso']: {
            config['INGREDIENT']['espresso']: 9,
            config['INGREDIENT']['16oz_cup']: 1
    },
    config['COFFEE']['iced_doppio']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['16oz_cup']: 1
    },
    config['COFFEE']['iced_macchiato']: {
            config['INGREDIENT']['espresso']: 9,
            config['INGREDIENT']['16oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 2
    },
    config['COFFEE']['iced_doppio_macchiato']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['16oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 2
    },
    config['COFFEE']['iced_cortado']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['16oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 4
    },
    config['COFFEE']['iced_cappuccino']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['16oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 4
    },
    config['COFFEE']['iced_flat_white']: {
            config['INGREDIENT']['espresso']: 27,
            config['INGREDIENT']['16oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 8
    },
    config['COFFEE']['iced_pour_over']: {
            config['INGREDIENT']['espresso']: 15,
            config['INGREDIENT']['16oz_cup']: 1
    },
    config['COFFEE']['iced_americano']: {
            config['INGREDIENT']['espresso']: 27,
            config['INGREDIENT']['16oz_cup']: 1,
    },
    config['COFFEE']['iced_latte']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['16oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 8
    },
    config['COFFEE']['iced_mocha']: {
            config['INGREDIENT']['espresso']: 18,
            config['INGREDIENT']['16oz_cup']: 1,
            config['INGREDIENT']['whole_milk']: 8,
            config['INGREDIENT']['chocolate_syrup']: 4,
    },
    config['COFFEE']['iced_red_eye']: {
            config['INGREDIENT']['espresso']: 27,
            config['INGREDIENT']['16oz_cup']: 1,
    },
    config['COFFEE']['iced_black_eye']: {
            config['INGREDIENT']['espresso']: 36,
            config['INGREDIENT']['16oz_cup']: 1,
    }
    # config['COFFEE']['iced_matcha_latte']: [
    #     {
    #         config['INGREDIENT']['espresso']: 18,
    #         config['INGREDIENT']['16oz_cup']: 1,
    #         config['INGREDIENT']['whole_milk']: 8
    #     }
    # ],
    # config['COFFEE']['iced_hojicha_latte']: [
    #     {
    #         config['INGREDIENT']['espresso']: 18,
    #         config['INGREDIENT']['16oz_cup']: 1,
    #         config['INGREDIENT']['whole_milk']: 8
    #     }
    # ],
    # config['COFFEE']['iced_chai_latte']: [
    #     {
    #         config['INGREDIENT']['espresso']: 18,
    #         config['INGREDIENT']['16oz_cup']: 1,
    #         config['INGREDIENT']['whole_milk']: 8
    #     }
    # ]
}

global coffee_list
coffee_list = [
    config['COFFEE']['hot_espresso'],
    config['COFFEE']['iced_espresso'],
    config['COFFEE']['hot_doppio'],
    config['COFFEE']['iced_doppio'],
    config['COFFEE']['hot_macchiato'],
    config['COFFEE']['iced_macchiato'],
    config['COFFEE']['hot_doppio_macchiato'],
    config['COFFEE']['iced_doppio_macchiato'],

    config['COFFEE']['hot_cortado'],
    config['COFFEE']['iced_cortado'],
    config['COFFEE']['hot_cappuccino'],
    config['COFFEE']['iced_cappuccino'],
    config['COFFEE']['hot_flat_white'],
    config['COFFEE']['iced_flat_white'],
    config['COFFEE']['hot_pour_over'],
    config['COFFEE']['iced_pour_over'],

    config['COFFEE']['hot_americano'],
    config['COFFEE']['iced_americano'],
    config['COFFEE']['hot_latte'],
    config['COFFEE']['iced_latte'],
    config['COFFEE']['hot_mocha'],
    config['COFFEE']['iced_mocha'],
    config['COFFEE']['hot_red_eye'],
    config['COFFEE']['iced_red_eye'],
    config['COFFEE']['hot_black_eye'],
    config['COFFEE']['iced_black_eye']
]

global modifier_milk_list
modifier_milk_list = {
    config['MODIFIER']['regular_modification']: config['INGREDIENT']['whole_milk'], #Whole Milk
    config['MODIFIER']['oat_modification']: config['INGREDIENT']['oat_milk'], #Oat
    config['MODIFIER']['almond_modification']: config['INGREDIENT']['almond_milk'], #Almond
    config['MODIFIER']['soy_modification']: config['INGREDIENT']['soy_milk'], #Soy
}

global modifier_syrup_list
modifier_syrup_list = {
    config['MODIFIER']['vanilla_modification']: config['INGREDIENT']['vanilla_syrup'], #vanilla
    config['MODIFIER']['caramel_modification']: config['INGREDIENT']['caramel_syrup'], #caramel
    config['MODIFIER']['hazelnut_modification']: config['INGREDIENT']['hazelnut_syrup'],#hazelnut
    config['MODIFIER']['chocolate_modification']: config['INGREDIENT']['chocolate_syrup'], #chocolate
    config['MODIFIER']['seasonal_modification']: config['INGREDIENT']['seasonal_syrup'] #seasonal
}

global modifier_shot_list
modifier_shot_list = {
    config['MODIFIER']['extra_single_modification']: config['INGREDIENT']['espresso'], #single
    config['MODIFIER']['extra_double_modification']: config['INGREDIENT']['espresso'] #double
}

global all_modifiers
all_modifiers = {
    config['MODIFIER']['regular_modification']: config['INGREDIENT']['whole_milk'],  # Whole Milk
    config['MODIFIER']['oat_modification']: config['INGREDIENT']['oat_milk'],  # Oat
    config['MODIFIER']['almond_modification']: config['INGREDIENT']['almond_milk'],  # Almond
    config['MODIFIER']['soy_modification']: config['INGREDIENT']['soy_milk'],  # Soy

    config['MODIFIER']['vanilla_modification']: config['INGREDIENT']['vanilla_syrup'],  # vanilla
    config['MODIFIER']['caramel_modification']: config['INGREDIENT']['caramel_syrup'],  # caramel
    config['MODIFIER']['hazelnut_modification']: config['INGREDIENT']['hazelnut_syrup'],  # hazelnut
    config['MODIFIER']['chocolate_modification']: config['INGREDIENT']['chocolate_syrup'],  # chocolate
    config['MODIFIER']['seasonal_modification']: config['INGREDIENT']['seasonal_syrup'],  # seasonal

    config['MODIFIER']['extra_single_modification']: config['INGREDIENT']['espresso'],  # single
    config['MODIFIER']['extra_double_modification']: config['INGREDIENT']['espresso']  # double
}

global item_list_count
item_list_count = {
    config['COFFEE']['hot_espresso']: 0,
    config['COFFEE']['iced_espresso']: 0,
    config['COFFEE']['hot_doppio']: 0,
    config['COFFEE']['iced_doppio']: 0,
    config['COFFEE']['hot_macchiato']: 0,
    config['COFFEE']['iced_macchiato']: 0,
    config['COFFEE']['hot_doppio_macchiato']: 0,
    config['COFFEE']['iced_doppio_macchiato']: 0,

    config['COFFEE']['hot_cortado']: 0,
    config['COFFEE']['iced_cortado']: 0,
    config['COFFEE']['hot_cappuccino']: 0,
    config['COFFEE']['iced_cappuccino']: 0,
    config['COFFEE']['hot_flat_white']: 0,
    config['COFFEE']['iced_flat_white']: 0,
    config['COFFEE']['hot_pour_over']: 0,
    config['COFFEE']['iced_pour_over']: 0,

    config['COFFEE']['hot_americano']: 0,
    config['COFFEE']['iced_americano']: 0,
    config['COFFEE']['hot_latte']: 0,
    config['COFFEE']['iced_latte']: 0,
    config['COFFEE']['hot_mocha']: 0,
    config['COFFEE']['iced_mocha']: 0,
    config['COFFEE']['hot_red_eye']: 0,
    config['COFFEE']['iced_red_eye']: 0,
    config['COFFEE']['hot_black_eye']: 0,
    config['COFFEE']['iced_black_eye']: 0
}

global modifier_list_count
modifier_list_count = {
    config['MODIFIER']['regular_modification']: 0,  # Whole Milk
    config['MODIFIER']['oat_modification']: 0,  # Oat
    config['MODIFIER']['almond_modification']: 0,  # Almond
    config['MODIFIER']['soy_modification']: 0,  # Soy
    config['MODIFIER']['vanilla_modification']: 0,  # vanilla
    config['MODIFIER']['caramel_modification']: 0,  # caramel
    config['MODIFIER']['hazelnut_modification']: 0,  # hazelnut
    config['MODIFIER']['chocolate_modification']: 0,  # chocolate
    config['MODIFIER']['seasonal_modification']: 0,  # seasonal
    config['MODIFIER']['extra_single_modification']: 0,  # single
    config['MODIFIER']['extra_double_modification']: 0  # double
}

global modifier_names
modifier_names = {
        config['MODIFIER']['regular_modification']: 'regular milk',
        config['MODIFIER']['oat_modification']: 'oat milk',
        config['MODIFIER']['almond_modification']: 'almond milk',
        config['MODIFIER']['soy_modification']: 'soy milk',
        config['MODIFIER']['vanilla_modification']: 'vanilla syrup',
        config['MODIFIER']['caramel_modification']: 'caramel syrup',
        config['MODIFIER']['hazelnut_modification']: 'hazelnut syrup',
        config['MODIFIER']['chocolate_modification']: 'chocolate syrup',
        config['MODIFIER']['seasonal_modification']: 'seasonal syrup',
        config['MODIFIER']['extra_single_modification']: 'extra single shot',
        config['MODIFIER']['extra_double_modification']: 'extra double shot'
}

global milk_ingredients
milk_ingredients = [
    config['INGREDIENT']['whole_milk'],
    config['INGREDIENT']['oat_milk'],
    config['INGREDIENT']['almond_milk'],
    config['INGREDIENT']['soy_milk']
]

global syrup_ingredients
syrup_ingredients = [
    config['INGREDIENT']['vanilla_syrup'],
    config['INGREDIENT']['caramel_syrup'],
    config['INGREDIENT']['hazelnut_syrup'],
    config['INGREDIENT']['chocolate_syrup'],
    config['INGREDIENT']['seasonal_syrup']
]

global shot_ingredients
shot_ingredients = [
    config['INGREDIENT']['espresso']
]

global ingredient_names
ingredient_names={
    config['INGREDIENT']['espresso']: 'espresso',
    config['INGREDIENT']['whole_milk']: 'whole milk',
    config['INGREDIENT']['oat_milk']: 'oat milk',
    config['INGREDIENT']['almond_milk']: 'almond milk',
    config['INGREDIENT']['soy_milk']: 'soy milk',
    config['INGREDIENT']['4oz_cup']: '4oz cup',
    config['INGREDIENT']['6oz_cup']: '6oz cup',
    config['INGREDIENT']['12oz_cup']: '12oz cup',
    config['INGREDIENT']['16oz_cup']: '16oz cup',
    config['INGREDIENT']['vanilla_syrup']: 'vanilla syrup',
    config['INGREDIENT']['caramel_syrup']: 'caramel syrup',
    config['INGREDIENT']['hazelnut_syrup']: 'hazelnut syrup',
    config['INGREDIENT']['chocolate_syrup']: 'chocolate syrup',
    config['INGREDIENT']['seasonal_syrup']: 'seasonal syrup'
}

simulator_columns = [
    'Timestamp',
    'Location_id',
    'Location_name',
    'Reference_id',
    'Action',
    'Ingredient',
    'Amount',
    'Unit',
    'Order_id'
]

inventory_columns = [
    'Timestamp',
    'Reference_id',
    'Action',
    'Ingredient',
    'Amount',
    'Unit',
    'Order_id'
]

sales_report_columns = [
    'Name',
    'Quantity',
    'Price_per_unit',
    'Total'
]

FactSales_column = [
    'Order_id', #for accessing order info
    'Timestamp',
    'Reference_id', #for better readability
    'Product_name', #drink name
    'Modifiers',
    'Total_price',
    'Ingredient_cost',
    'Customer_id'
]

DimRecipe_column = [
    'Product_id',
    'Product_name',
    'Ingredient_id',
    'Ingredient_name',
]

DimIngredients_column = [
    'Id',
    'Name',
    'Unit',
    'PPU'
]

dtype_mapping = {
    'Timestamp': 'datetime64[ns]',
    'Reference_id': "string",
    'Action': "string",
    'Ingredient': 'string',
    'Amount': 'int64',
    'Unit': 'string',
    'Order_id': 'string'
}