import configparser
import os

#path reference to config.ini
config_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(config_dir, 'config.ini')

def load_config(path='config.ini'):
    config = configparser.ConfigParser()
    reference = config.read(config_path)
    if not reference:
        raise FileNotFoundError(f"Could not find config.ini at {config_path}")
    return config

