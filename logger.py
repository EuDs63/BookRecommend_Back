# config/logger.py

import logging


def create_logger(app):
    logger = logging.getLogger(app.name if app else __name__)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S' )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
