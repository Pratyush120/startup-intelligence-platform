"""
Google News Collector
"""

import re
import feedparser
from datetime import datetime, UTC

from config.config import Config
from src.collectors.base_collector import BaseCollector
from src.models.record import Record


class GoogleNewsCollector(BaseCollector):

    def __init__(self):

        self.feed_url = Config.GOOGLE_NEWS_RSS

    def fetch(self):

        return feedparser.parse(self.feed_url)

    def parse(self, feed):

        records = []

        for entry in feed.entries:

            record = Record(

                source="Google News",

                title=entry.get("title", "").strip(),

                description=re.sub(
                    "<.*?>",
                    "",
                    entry.get("summary", "")
                ),

                url=entry.get("link", ""),

                published_at=entry.get("published"),

                collected_at=datetime.now(
                    UTC
                ).isoformat(),

                record_type="news",

                metadata={
                    "publisher":
                    entry.get(
                        "source",
                        {}
                    ).get(
                        "title",
                        "Unknown"
                    )
                }

            )

            records.append(record)

        return records