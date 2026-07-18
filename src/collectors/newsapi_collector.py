"""
News API Collector

Fetches articles using the NewsAPI REST endpoint if credentials exist.
"""

from typing import List, Any
from urllib.parse import urlencode

from config.config import Config
from src.collectors.base_collector import BaseCollector
from src.models.record import Record


class NewsAPICollector(BaseCollector):
    def __init__(self, retries=3, backoff_factor=1.0, timeout=10):
        super().__init__(retries, backoff_factor, timeout)
        self.api_key = getattr(Config, "NEWS_API_KEY", None)
        self.base_url = "https://newsapi.org/v2/everything"
        # Search for AI and startup topics
        self.query = 'startup OR "artificial intelligence" OR funding OR acquisition'

    def fetch(self) -> Any:
        if not self.api_key:
            return None  # Graceful fallback, will be caught by pipeline

        params = {
            "q": self.query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 50,
            "apiKey": self.api_key,
        }

        response = self.session.get(
            f"{self.base_url}?{urlencode(params)}", timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def parse(self, raw_data: Any) -> List[Record]:
        if not raw_data or raw_data.get("status") != "ok":
            return []

        records = []
        for article in raw_data.get("articles", []):
            record = Record(
                source="NewsAPI",
                title=article.get("title", ""),
                description=article.get("description", ""),
                url=article.get("url", ""),
                published_at=article.get("publishedAt"),
                collected_at=self.get_timestamp(),
                record_type="news",
                metadata={
                    "publisher": article.get("source", {}).get("name", "Unknown")
                },
            )
            # Filter out records with removed content
            if (
                "[Removed]" not in record.title
                and "[Removed]" not in record.description
            ):
                records.append(record)

        return records
