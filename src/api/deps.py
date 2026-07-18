from src.database.repository import Repository
from src.utils.logger import get_logger

logger = get_logger("api")


def get_repository() -> Repository:
    repo = Repository()
    try:
        yield repo
    finally:
        repo.close()


def get_api_logger():
    return logger
