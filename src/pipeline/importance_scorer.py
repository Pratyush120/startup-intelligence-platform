"""
Importance Scorer

Assigns a 0-100 importance score based on source authority, event type, recency, and confidence.
"""

from datetime import datetime, timezone
from typing import Optional

from src.models.record import Record
from src.utils.logger import get_logger

logger = get_logger(__name__)

SOURCE_AUTHORITY: dict[str, float] = {
    "techcrunch": 95,
    "bloomberg": 100,
    "reuters": 98,
    "financial times": 95,
    "wall street journal": 95,
    "wsj": 95,
    "the economic times": 80,
    "business standard": 75,
    "inc42": 70,
    "your story": 65,
    "yourstory": 65,
    "entrackr": 60,
    "venture beat": 85,
    "venturebeat": 85,
    "crunchbase": 80,
    "the information": 90,
    "wired": 75,
    "fortune": 80,
    "google news": 50,
}

EVENT_TYPE_WEIGHTS: dict[str, float] = {
    "IPO": 100,
    "Acquisition": 90,
    "Funding": 85,
    "Layoffs": 75,
    "Partnership": 65,
    "Expansion": 60,
    "Product Launch": 55,
    "Hiring": 50,
    "Leadership": 60,
    "Regulation": 70,
    "Security": 80,
    "General": 30,
}


class ImportanceScorer:
    RECENCY_HALF_LIFE_DAYS = 7

    def score(self, record: Record) -> float:
        """
        Returns a float 0.0-100.0 importance score.
        """
        source = record.source
        publisher = record.metadata.get("publisher", "")
        published_at = record.published_at
        event_type = record.metadata.get("category", "General")
        confidence = record.metadata.get("confidence", 0.5)

        source_score = self._source_authority(source, publisher)
        event_score = self._event_weight(event_type)
        recency_score = self._recency_score(published_at)

        # Base raw score 0-100
        raw = (
            source_score * 0.25
            + event_score * 0.40
            + recency_score * 0.20
            + (confidence * 100) * 0.15
        )

        return round(min(max(raw, 0.0), 100.0), 2)

    def _source_authority(self, source: str, publisher: str) -> float:
        combined = f"{publisher} {source}".lower()
        for known, score in SOURCE_AUTHORITY.items():
            if known in combined:
                return score
        return 50.0

    def _event_weight(self, event_type: str) -> float:
        return EVENT_TYPE_WEIGHTS.get(event_type, 40.0)

    def _recency_score(self, published_at: Optional[str]) -> float:
        if not published_at:
            return 50.0
        try:
            pub_dt = datetime.fromisoformat(str(published_at).replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            if pub_dt.tzinfo is None:
                pub_dt = pub_dt.replace(tzinfo=timezone.utc)
            age_days = (now - pub_dt).total_seconds() / 86400
            decay = 0.5 ** (age_days / self.RECENCY_HALF_LIFE_DAYS)
            return round(100.0 * decay, 2)
        except (ValueError, TypeError):
            return 50.0
