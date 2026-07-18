"""
Deduplicator

Prevents the same article from being re-processed on subsequent pipeline runs.

Two-pass deduplication:
  Pass 1 — URL hash (exact match against DB)
  Pass 2 — Title similarity (fuzzy match within the current batch)
"""

import hashlib
from difflib import SequenceMatcher
from typing import List, Set, Optional

from src.models.record import Record
from src.utils.logger import get_logger

logger = get_logger(__name__)


def url_hash(url: str) -> str:
    """Returns a stable SHA-256 hex digest of the URL."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def title_similarity(a: str, b: str) -> float:
    """Returns a 0.0-1.0 similarity ratio between two title strings."""
    return SequenceMatcher(
        None,
        a.lower().strip(),
        b.lower().strip()
    ).ratio()


class Deduplicator:

    TITLE_SIMILARITY_THRESHOLD = 0.85

    def __init__(self, existing_hashes: Optional[Set[str]] = None):
        """
        Args:
            existing_hashes: A set of url_hash strings already stored in the DB.
                             Loaded from Repository.get_all_url_hashes().
        """
        self.seen_hashes: Set[str] = existing_hashes or set()

    def deduplicate(self, records: List[Record]) -> List[Record]:
        """Returns a de-duplicated list of records."""
        unique: List[Record] = []
        batch_titles: List[str] = []
        removed = 0

        for record in records:
            h = url_hash(record.url or record.title)
            if h in self.seen_hashes:
                removed += 1
                continue

            is_duplicate = False
            for existing_title in batch_titles:
                if title_similarity(record.title, existing_title) >= self.TITLE_SIMILARITY_THRESHOLD:
                    is_duplicate = True
                    removed += 1
                    break

            if not is_duplicate:
                record.metadata["url_hash"] = h
                self.seen_hashes.add(h)
                batch_titles.append(record.title)
                unique.append(record)

        logger.info(
            f"Deduplicator: {len(unique)} unique, {removed} duplicates removed."
        )
        return unique
