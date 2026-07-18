"""
Base Collector

Defines the common workflow for all collectors with retry, timeout, and graceful failure logic.
"""

from abc import ABC, abstractmethod
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Any
from datetime import datetime, timezone

from src.models.record import Record
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseCollector(ABC):
    def __init__(self, retries=3, backoff_factor=1.0, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        retry = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def collect(self) -> List[Record]:
        logger.info(f"Starting {self.__class__.__name__}")

        try:
            raw_data = self.fetch()
            if not raw_data:
                logger.warning(f"{self.__class__.__name__} fetch returned empty data.")
                return []

            records = self.parse(raw_data)
            logger.info(f"{self.__class__.__name__} collected {len(records)} records.")
            return records
        except Exception as e:
            logger.error(f"{self.__class__.__name__} failed during collection: {e}")
            return []

    @abstractmethod
    def fetch(self) -> Any:
        pass

    @abstractmethod
    def parse(self, raw_data: Any) -> List[Record]:
        pass

    def get_timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()
