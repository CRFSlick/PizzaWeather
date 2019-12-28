import json


class Config:
    with open('config.json') as config_file:
        config = json.load(config_file)

    OPENWEATHERMAP_API_KEY = config.get('openweathermap_api_key')
    RAPID_API_KEY = config.get('rapid_api_key')

