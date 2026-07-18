"""
Google News RSS Collector
"""

import re
import feedparser

from config.config import Config
from src.collectors.base_collector import BaseCollector
from src.models.record import Record


class GoogleNewsCollector(BaseCollector):
    def __init__(self, retries=3, backoff_factor=1.0, timeout=10):
        super().__init__(retries, backoff_factor, timeout)
        self.feed_url = getattr(
            Config,
            "GOOGLE_NEWS_RSS",
            "https://news.google.com/rss/search?q=startups+OR+funding+OR+acquisition+when:1d&hl=en-US&gl=US&ceid=US:en",
        )

    def fetch(self):
        try:
            response = self.session.get(self.feed_url, timeout=self.timeout)
            response.raise_for_status()
            return feedparser.parse(response.content)
        except Exception:
            return None

    def parse(self, feed):
        if not feed or not feed.entries:
            return []

        records = []
        for entry in feed.entries:
            record = Record(
                source="Google News",
                title=entry.get("title", "").strip(),
                description=re.sub("<.*?>", " ", entry.get("summary", "")).strip(),
                url=entry.get("link", ""),
                published_at=entry.get("published"),
                collected_at=self.get_timestamp(),
                record_type="news",
                metadata={"publisher": entry.get("source", {}).get("title", "Unknown")},
            )
            records.append(record)

        return records
