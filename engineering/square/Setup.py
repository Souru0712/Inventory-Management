from config.Config_loader import load_config
from engineering.Dag_scheduler import complete_order
from Locations import create_location
from Inventory import create_inventory
from Items import create_items
from Orders import create_first_order

config = load_config()

def setup():
    #1. create location. Locations and Orders within a location cannot be deleted. They can only be modified

    create_location()

    #2. create items for your location. This is essential for creating orders.
    # Each item will have an unique code. Duplicates will complicate tracking.
    #warning: this deletes all previous item codes but keeps existing locations

    create_items()

    #3. set inventory for your ingredients. This will be your digital inventory room.
    # Additional research is required to determine your distributors, ingredient brands and amounts, and total pricing

    create_inventory()

    #4. Modify your structures files to adjust your recipe book, assuming each product uses exact ingredients.
    # During order creation, you could modify the ingredients separately there



    #5. start the first ticket number. This is a simple program that sends a
    # sample request to Square while also:
    # i. making sure the recipe book works
    # ii. API calls are successful
    # iii. sets a starting point for tracking ticket numbers (optional, but I think it keeps sales organized in a systematic matter)

    receipt = create_first_order()

    #6. Complete the order. Orders have states: [OPEN, CLOSED, REFUNDED, COMPLETED, etc]. The function simulates transaction
    # and is suitable for real-life sales tracking for later reports

    complete_order(receipt)

if __name__ == '__main__':
    setup()