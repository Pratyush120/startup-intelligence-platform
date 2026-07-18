"""
Base Collector

Defines the common workflow for all collectors.
"""

from abc import ABC, abstractmethod

from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseCollector(ABC):

    def collect(self):

        logger.info(f"Starting {self.__class__.__name__}")

        raw_data = self.fetch()

        records = self.parse(raw_data)

        logger.info(
            f"{self.__class__.__name__} collected {len(records)} records."
        )

        return records

    @abstractmethod
    def fetch(self):
        pass

    @abstractmethod
    def parse(self, raw_data):
        pass