"""
Importance Scorer

Assigns a 0-10 importance score based on source authority, event type, and recency.
"""

from datetime import datetime, timezone
from typing import Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)

SOURCE_AUTHORITY: dict[str, float] = {
    "techcrunch": 9.5,
    "bloomberg": 10.0,
    "reuters": 9.8,
    "financial times": 9.5,
    "wall street journal": 9.5,
    "wsj": 9.5,
    "the economic times": 8.0,
    "business standard": 7.5,
    "inc42": 7.0,
    "your story": 6.5,
    "yourstory": 6.5,
    "entrackr": 6.0,
    "venture beat": 8.5,
    "venturebeat": 8.5,
    "crunchbase": 8.0,
    "the information": 9.0,
    "wired": 7.5,
    "fortune": 8.0,
    "google news": 5.0,
}

EVENT_TYPE_WEIGHTS: dict[str, float] = {
    "IPO": 10.0,
    "Acquisition": 9.0,
    "Funding": 8.0,
    "Layoff": 7.5,
    "Partnership": 6.5,
    "Expansion": 6.0,
    "Product Launch": 5.5,
    "Hiring": 5.0,
    "Leadership": 6.0,
    "Litigation": 7.0,
    "General": 3.0,
}


class ImportanceScorer:

    RECENCY_HALF_LIFE_DAYS = 7

    def score(
        self,
        source: str = "",
        publisher: str = "",
        published_at: Optional[str] = None,
        event_type: str = "General",
    ) -> float:
        """
        Returns a float 0.0-10.0 importance score.

        Args:
            source: Source name (e.g., 'Google News')
            publisher: Publisher name (e.g., 'TechCrunch')
            published_at: ISO datetime string
            event_type: Detected event type
        """
        source_score = self._source_authority(source, publisher)
        event_score = self._event_weight(event_type)
        recency_score = self._recency_score(published_at)

        raw = (
            source_score * 0.30
            + event_score * 0.40
            + recency_score * 0.30
        )

        return round(min(max(raw, 0.0), 10.0), 2)

    def _source_authority(self, source: str, publisher: str) -> float:
        combined = f"{publisher} {source}".lower()
        for known, score in SOURCE_AUTHORITY.items():
            if known in combined:
                return score
        return 5.0

    def _event_weight(self, event_type: str) -> float:
        return EVENT_TYPE_WEIGHTS.get(event_type, 4.0)

    def _recency_score(self, published_at: Optional[str]) -> float:
        if not published_at:
            return 5.0
        try:
            pub_dt = datetime.fromisoformat(
                str(published_at).replace("Z", "+00:00")
            )
            now = datetime.now(timezone.utc)
            if pub_dt.tzinfo is None:
                pub_dt = pub_dt.replace(tzinfo=timezone.utc)
            age_days = (now - pub_dt).total_seconds() / 86400
            decay = 0.5 ** (age_days / self.RECENCY_HALF_LIFE_DAYS)
            return round(10.0 * decay, 2)
        except (ValueError, TypeError):
            return 5.0
