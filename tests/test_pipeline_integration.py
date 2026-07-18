"""
Integration test for the SDIP pipeline.

Runs the preprocessor, deduplicator, and importance scorer on mocked records.
Does NOT call LLM or the database.
"""

import unittest
from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime, timezone

from src.pipeline.preprocessor import Preprocessor
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.importance_scorer import ImportanceScorer
from src.pipeline.llm_analyzer import LLMAnalyzer, LLMAnalysis
from src.pipeline.sparkline_generator import SparklineGenerator


@dataclass
class MockRecord:
    source: str = "Google News"
    title: str = ""
    description: str = ""
    url: str = ""
    published_at: Optional[str] = None
    collected_at: str = ""
    record_type: str = "news"
    metadata: Dict = field(default_factory=dict)


class TestPipelineIntegration(unittest.TestCase):
    def test_full_preprocessing_flow(self):
        now = datetime.now(timezone.utc).isoformat()
        records = [
            MockRecord(
                title="Stripe raises $2B in Series G",
                description="<p>Stripe has <b>raised</b> $2B.</p>",
                url="https://example.com/1",
                published_at=now,
                collected_at=now,
            ),
            MockRecord(
                title="Stripe raises $2B in Series G funding",
                description="Stripe raised 2 billion.",
                url="https://example.com/2",
                published_at=now,
                collected_at=now,
            ),
            MockRecord(
                title="",
                description="Empty title article",
                url="https://example.com/3",
                published_at=now,
                collected_at=now,
            ),
        ]

        preprocessor = Preprocessor()
        cleaned = preprocessor.process(records)
        self.assertLessEqual(len(cleaned), 3)

        dedup = Deduplicator()
        unique = dedup.deduplicate(cleaned)
        self.assertLessEqual(len(unique), len(cleaned))

        scorer = ImportanceScorer()
        for record in unique:
            record.metadata["category"] = "Funding"
            score = scorer.score(record)
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)


class TestLLMFallback(unittest.TestCase):
    def test_rule_based_fallback_returns_analysis(self):
        analyzer = LLMAnalyzer()
        result = analyzer.analyze(
            title="OpenAI raises $6.6B",
            description="OpenAI raised $6.6 billion.",
            event_type="Funding",
            company="OpenAI",
        )
        self.assertIsInstance(result, LLMAnalysis)
        self.assertGreater(len(result.executive_summary), 0)
        self.assertGreater(len(result.business_impact), 0)
        self.assertGreater(result.confidence, 0.0)
        self.assertIsInstance(result.risk, str)
        self.assertIsInstance(result.opportunity, str)


class TestSparklineGenerator(unittest.TestCase):
    def test_returns_five_points(self):
        gen = SparklineGenerator()
        result = gen.generate([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.assertEqual(len(result), 5)

    def test_empty_history_returns_defaults(self):
        gen = SparklineGenerator()
        result = gen.generate([])
        self.assertEqual(len(result), 5)
        self.assertTrue(all(v == 50.0 for v in result))

    def test_short_history_pads(self):
        gen = SparklineGenerator()
        result = gen.generate([80, 90])
        self.assertEqual(len(result), 5)

    def test_normalized_range(self):
        gen = SparklineGenerator()
        result = gen.generate([10, 20, 30, 40, 50])
        self.assertTrue(all(0 <= v <= 100 for v in result))


if __name__ == "__main__":
    unittest.main()
