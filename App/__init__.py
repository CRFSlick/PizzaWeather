from flask import Flask
from App.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from App.routes.routes import main

app.register_blueprint(main)