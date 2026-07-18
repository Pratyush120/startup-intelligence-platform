"""
Tests for ImportanceScorer
"""

from datetime import datetime, timezone, timedelta
from src.pipeline.importance_scorer import ImportanceScorer
from src.models.record import Record


class TestImportanceScorer:
    def setup_method(self):
        self.scorer = ImportanceScorer()

    def _make_record(
        self, source, publisher, event_type, published_at=None, confidence=0.8
    ):
        if not published_at:
            published_at = datetime.now(timezone.utc).isoformat()
        return Record(
            source=source,
            title="Test",
            description="",
            url="url",
            published_at=published_at,
            collected_at="",
            record_type="news",
            metadata={
                "publisher": publisher,
                "category": event_type,
                "confidence": confidence,
            },
        )

    def test_high_authority_source(self):
        record = self._make_record("Bloomberg", "Bloomberg", "IPO")
        score = self.scorer.score(record)
        assert score > 80.0

    def test_low_authority_source(self):
        record = self._make_record("Unknown Blog", "Unknown", "General")
        score = self.scorer.score(record)
        assert score < 60.0

    def test_event_weights(self):
        r1 = self._make_record("TechCrunch", "TechCrunch", "Funding")
        r2 = self._make_record("TechCrunch", "TechCrunch", "General")
        score1 = self.scorer.score(r1)
        score2 = self.scorer.score(r2)
        assert score1 > score2

    def test_recency_decay(self):
        now = datetime.now(timezone.utc)
        old_date = (now - timedelta(days=14)).isoformat()
        r_new = self._make_record(
            "TechCrunch", "TechCrunch", "Funding", now.isoformat()
        )
        r_old = self._make_record("TechCrunch", "TechCrunch", "Funding", old_date)

        score_new = self.scorer.score(r_new)
        score_old = self.scorer.score(r_old)
        assert score_new > score_old

    def test_invalid_date_graceful_handling(self):
        record = self._make_record(
            "TechCrunch", "TechCrunch", "Funding", "invalid-date-format"
        )
        score = self.scorer.score(record)
        assert isinstance(score, float)
