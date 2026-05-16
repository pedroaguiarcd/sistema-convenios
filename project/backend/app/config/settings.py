import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database/convenios.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # Monitoramento
    DIAS_ALERTA_VENCIMENTO = int(os.getenv("DIAS_ALERTA_VENCIMENTO", 30))
    SCHEDULER_ENABLED = os.getenv("SCHEDULER_ENABLED", "True").lower() == "true"
    SCHEDULER_INTERVAL_HOURS = int(os.getenv("SCHEDULER_INTERVAL_HOURS", 24))

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)
