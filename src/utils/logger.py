import logging
from pathlib import Path

from config.config import Config


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.
    """

    # Create logs directory if it doesn't exist
    Path(Config.LOG_DIR).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(Config.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        Config.LOG_DIR / "app.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger