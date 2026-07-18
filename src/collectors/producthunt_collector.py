"""
Product Hunt Collector Stub

Reserved for future extensibility.
"""

from typing import List, Any
from src.collectors.base_collector import BaseCollector
from src.models.record import Record


class ProductHuntCollector(BaseCollector):
    def fetch(self) -> Any:
        return []

    def parse(self, raw_data: Any) -> List[Record]:
        return []
