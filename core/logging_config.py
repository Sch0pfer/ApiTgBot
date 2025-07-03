import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                "app.log",
                maxBytes=1024 * 1024 * 5,
                backupCount=10,
            ),
            logging.StreamHandler(),
        ],
    )
