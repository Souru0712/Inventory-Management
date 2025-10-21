# Steps

1. Make sure to rename the config.example.ini file -> config.ini. This will allow the config_loader to be able to reference the file and access keys and secrets that you set.

2. Modify the credentials in your config.ini file:

    - Find your Google email app_password to initiate a request which should match the sender email.
        The receiver email is the email you want to send to
    - Create a Square account to retrieve your api_key and have access to the sandbox mode.
        NOTE: production mode requires payment for activation in order to accept transactions from
          customers
    - The menu items, modifiers, and ingredients are later created when running Setup.py, which will also            store the ID's of the created objects so they are easier to reference in the API

