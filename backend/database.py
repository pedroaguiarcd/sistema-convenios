from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from backend.config import Config


db = SQLAlchemy()


def criar_app_flask():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    return app