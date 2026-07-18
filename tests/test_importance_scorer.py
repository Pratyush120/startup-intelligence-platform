"""
Tests for ImportanceScorer
"""

import unittest
from datetime import datetime, timezone, timedelta

from src.pipeline.importance_scorer import ImportanceScorer


class TestImportanceScorer(unittest.TestCase):

    def setUp(self):
        self.scorer = ImportanceScorer()

    def test_returns_float_in_range(self):
        score = self.scorer.score(source="Google News", event_type="Funding")
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 10.0)

    def test_techcrunch_scores_higher_than_unknown(self):
        tc = self.scorer.score(publisher="TechCrunch", event_type="Funding")
        unknown = self.scorer.score(publisher="Random Blog", event_type="Funding")
        self.assertGreater(tc, unknown)

    def test_acquisition_scores_higher_than_hiring(self):
        acq = self.scorer.score(event_type="Acquisition")
        hire = self.scorer.score(event_type="Hiring")
        self.assertGreater(acq, hire)

    def test_ipo_is_highest_weight(self):
        ipo = self.scorer.score(event_type="IPO")
        funding = self.scorer.score(event_type="Funding")
        self.assertGreater(ipo, funding)

    def test_recent_article_scores_higher(self):
        now = datetime.now(timezone.utc).isoformat()
        old = (datetime.now(timezone.utc) - timedelta(days=14)).isoformat()
        recent = self.scorer.score(published_at=now, event_type="Funding")
        stale = self.scorer.score(published_at=old, event_type="Funding")
        self.assertGreater(recent, stale)

    def test_no_published_at_returns_neutral(self):
        score = self.scorer.score(event_type="General")
        self.assertGreater(score, 0.0)

    def test_bloomberg_is_max_authority(self):
        bloom = self.scorer.score(publisher="Bloomberg", event_type="General")
        generic = self.scorer.score(publisher="Unknown", event_type="General")
        self.assertGreater(bloom, generic)


if __name__ == "__main__":
    unittest.main()
