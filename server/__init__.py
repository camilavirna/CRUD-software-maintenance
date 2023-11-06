import logging

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config as Config

# carrega as variavéis de .env
load_dotenv()

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s %(funcName)s(): %(message)s", level=logging.INFO
)

db = SQLAlchemy()


def create_server(config_name):
    app = Flask(__name__)
    config_object = Config[config_name]()
    app.config.from_object(config_object)
    Config[config_name].init_app()
    db.init_app(app)

    return app
