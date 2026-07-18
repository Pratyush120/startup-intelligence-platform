"""
Tests for Deduplicator
"""

import unittest
from dataclasses import dataclass, field
from typing import Dict, Optional

from src.pipeline.deduplicator import Deduplicator, url_hash, title_similarity


@dataclass
class MockRecord:
    source: str = "test"
    title: str = ""
    description: str = ""
    url: str = ""
    published_at: Optional[str] = None
    collected_at: str = "2026-01-01"
    record_type: str = "news"
    metadata: Dict = field(default_factory=dict)


class TestUrlHash(unittest.TestCase):

    def test_deterministic(self):
        h1 = url_hash("https://example.com/article")
        h2 = url_hash("https://example.com/article")
        self.assertEqual(h1, h2)

    def test_different_urls_differ(self):
        h1 = url_hash("https://a.com")
        h2 = url_hash("https://b.com")
        self.assertNotEqual(h1, h2)


class TestTitleSimilarity(unittest.TestCase):

    def test_identical_titles(self):
        self.assertAlmostEqual(title_similarity("Hello World", "Hello World"), 1.0)

    def test_similar_titles(self):
        score = title_similarity(
            "OpenAI raises $6.6 billion in new funding",
            "OpenAI raises $6.6B in new funding round"
        )
        self.assertGreater(score, 0.8)

    def test_different_titles(self):
        score = title_similarity(
            "Tesla announces new factory",
            "Apple launches iPhone 20"
        )
        self.assertLess(score, 0.5)


class TestDeduplicator(unittest.TestCase):

    def test_removes_exact_url_duplicates(self):
        records = [
            MockRecord(title="Article 1", url="https://example.com/1"),
            MockRecord(title="Article 2", url="https://example.com/1"),
        ]
        dedup = Deduplicator()
        result = dedup.deduplicate(records)
        self.assertEqual(len(result), 1)

    def test_removes_similar_titles(self):
        records = [
            MockRecord(title="OpenAI raises $6.6 billion in new funding", url="https://a.com"),
            MockRecord(title="OpenAI raises $6.6B in new funding round", url="https://b.com"),
        ]
        dedup = Deduplicator()
        result = dedup.deduplicate(records)
        self.assertEqual(len(result), 1)

    def test_keeps_different_articles(self):
        records = [
            MockRecord(title="Tesla builds new factory", url="https://a.com"),
            MockRecord(title="Apple launches new product", url="https://b.com"),
        ]
        dedup = Deduplicator()
        result = dedup.deduplicate(records)
        self.assertEqual(len(result), 2)

    def test_seeded_hashes_prevent_reprocessing(self):
        h = url_hash("https://example.com/old")
        records = [
            MockRecord(title="Old Article", url="https://example.com/old"),
            MockRecord(title="New Article", url="https://example.com/new"),
        ]
        dedup = Deduplicator(existing_hashes={h})
        result = dedup.deduplicate(records)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "New Article")

    def test_url_hash_stored_in_metadata(self):
        records = [MockRecord(title="Test", url="https://test.com")]
        dedup = Deduplicator()
        result = dedup.deduplicate(records)
        self.assertIn("url_hash", result[0].metadata)


if __name__ == "__main__":
    unittest.main()
