"""
GitHub Collector Stub

Reserved for future extensibility to track open source repositories.
"""

from typing import List, Any
from src.collectors.base_collector import BaseCollector
from src.models.record import Record


class GithubCollector(BaseCollector):
    def fetch(self) -> Any:
        return []

    def parse(self, raw_data: Any) -> List[Record]:
        return []
