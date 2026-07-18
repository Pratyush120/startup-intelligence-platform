"""
Mock Collector

Provides static fixture data for robust testing without external dependencies.
"""

from typing import List, Any
from datetime import datetime, timezone

from src.collectors.base_collector import BaseCollector
from src.models.record import Record


class MockCollector(BaseCollector):
    def fetch(self) -> Any:
        # Simulate network delay if desired, but keep it instant for fast tests
        return [
            {
                "title": "OpenAI acquires search startup Global Illumination",
                "summary": "AI giant OpenAI has acquired digital product company Global Illumination for an undisclosed sum, aiming to bolster its core engineering team.",
                "url": "https://example.com/openai-acquisition",
                "published": datetime.now(timezone.utc).isoformat(),
                "source": "TechCrunch Mock",
            },
            {
                "title": "Stripe raises $6.5B at $50B valuation",
                "summary": "Payments giant Stripe has raised $6.5 billion in a massive Series I round, though its valuation has been cut to $50 billion from a peak of $95 billion.",
                "url": "https://example.com/stripe-funding",
                "published": datetime.now(timezone.utc).isoformat(),
                "source": "WSJ Mock",
            },
            {
                "title": "Tech startup layoffs continue in Q3",
                "summary": "Multiple mid-stage startups have announced workforce reductions ranging from 10-20% as capital markets remain tight.",
                "url": "https://example.com/startup-layoffs",
                "published": datetime.now(timezone.utc).isoformat(),
                "source": "Bloomberg Mock",
            },
            {
                "title": "Duplicate: Stripe raises $6.5B at $50B valuation",
                "summary": "Payments giant Stripe has raised $6.5 billion in a massive Series I round, though its valuation has been cut to $50 billion from a peak of $95 billion.",
                "url": "https://example.com/stripe-funding-2",
                "published": datetime.now(timezone.utc).isoformat(),
                "source": "WSJ Mock",
            },
        ]

    def parse(self, raw_data: Any) -> List[Record]:
        records = []
        for item in raw_data:
            record = Record(
                source="MockSource",
                title=item.get("title", ""),
                description=item.get("summary", ""),
                url=item.get("url", ""),
                published_at=item.get("published"),
                collected_at=self.get_timestamp(),
                record_type="news",
                metadata={"publisher": item.get("source", "Unknown")},
            )
            records.append(record)
        return records
