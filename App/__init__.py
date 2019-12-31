from App.modules.helper.helper import determine_slash_type
from flask import Flask
import json

app = Flask(__name__)
slash = determine_slash_type()


class Config:
    with open(f'{app.root_path}{slash}config{slash}config.json') as config_file:
        config = json.load(config_file)

    OPENWEATHERMAP_API_KEY = config.get('openweathermap_api_key')
    RAPID_API_KEY = config.get('rapid_api_key')


# Configure the application with API keys
app.config.from_object(Config)

# Register application routes
from App.routes.routes import main
app.register_blueprint(main)
