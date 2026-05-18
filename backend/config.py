import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "defaut_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = SECRET_KEY
    K=JWT_ACESS_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_EXPIRATION", 1))
    )

    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
    MAIL_USE_TLS =  os.getenv("MAIL_USE_TLS", "false").lower == "true"
    MAIL_USE_SSL =  os.getenv("MAIL_USE_SSL", "false").lower == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

    DAYS_ALERT_DUE = int(os.getenv("DAYS_ALERT_DUE", 7))

class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):

    DEBUG = False
    SQLALCHEMY_ECHO = False
