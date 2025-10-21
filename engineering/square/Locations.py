from square.client import Square
from square.environment import SquareEnvironment
from square.locations.client import LocationsClient

from config.Config_loader import load_config

config = load_config()

#Set the environment
client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=config['SQUARE']['api_key']
)

def input_location():
    business_name = input("Enter your business name: ").capitalize()
    business_email = input("Enter your business email: ").capitalize()
    description = input("Enter a description for your business: ").capitalize()
    instagram_username = input("Enter an instagram username: ").capitalize()
    address = {}
    address['address_line1']= input("Enter address_line1: ").capitalize()
    address['address_line2']= input("Enter address_line2: ").capitalize()
    address['postal_code']= input("Enter zip code: ")
    address['country']= input("Enter country: ").upper()
    address['administrative_district_level1']= input("Enter your city: ").capitalize()
    address['administrative_district_level2']= input("Enter your state: ").upper()
    address['locality']= input("Enter your neighborhood: ").capitalize()
    status = 'ACTIVE' #to activate the location
    name = input("Enter a name: ").capitalize()

    return business_name, business_email, description, instagram_username, address, status, name

def create_location():
    (business_name, business_email, description, instagram_username, address, status, name) = input_location()
    try:
        response = client.locations.create(
            location={
                "type": "PHYSICAL",
                "business_name": business_name,
                "business_email": business_email,
                "description": description,
                "instagram_username": instagram_username,
                "address": address,
                "status": status,
                "name": name
            }
        )

        config['LOCATION']['main'] = response.location_id
        with open('../../config/config.ini', 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        print(f'location creation failed: {e}')

def view_location():
    for location in client.locations.list().locations:
        print(location.name+' '+location.id)

def test_location():
    (business_name, business_email, description, instagram_username, address, status, name) = input_location()
    response = LocationsClient(
        location = {
            "type": "PHYSICAL",
            "business_name": business_name,
            "business_email": business_email,
            "description": description,
            "instagram_username": instagram_username,
            "address": address,
            "status": status,
            "name": name
        })

    # print(location)
    # view_location()
    return response.location.id

if __name__ == '__main__':
    test_location()
    view_location()