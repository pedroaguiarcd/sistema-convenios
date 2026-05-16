import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    log_level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # File handler
    log_dir = os.path.join(os.path.dirname(__file__), "../../logs")
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
