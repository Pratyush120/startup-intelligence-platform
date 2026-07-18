"""
Deduplicator

Prevents the same article from being re-processed on subsequent pipeline runs.

Two-pass deduplication:
  Pass 1 - URL hash (exact match against DB)
  Pass 2 - Similarity detection (rapidfuzz match within the current batch on title, description, URL, date)
"""

import hashlib
from rapidfuzz import fuzz
from typing import List, Set, Optional

from src.models.record import Record
from src.utils.logger import get_logger

logger = get_logger(__name__)


def url_hash(url: str) -> str:
    """Returns a stable SHA-256 hex digest of the URL."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def title_similarity(a: str, b: str) -> float:
    """Returns a 0.0-1.0 similarity ratio between two title strings."""
    if not a or not b:
        return 0.0
    return fuzz.token_sort_ratio(a.lower().strip(), b.lower().strip()) / 100.0


def text_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return fuzz.partial_ratio(a.lower().strip(), b.lower().strip()) / 100.0


class Deduplicator:
    TITLE_SIMILARITY_THRESHOLD = 0.80
    DESC_SIMILARITY_THRESHOLD = 0.85

    def __init__(self, existing_hashes: Optional[Set[str]] = None):
        """
        Args:
            existing_hashes: A set of url_hash strings already stored in the DB.
                             Loaded from Repository.get_all_url_hashes().
        """
        self.seen_hashes: Set[str] = existing_hashes or set()

    def deduplicate(self, records: List[Record]) -> List[Record]:
        """Returns a de-duplicated list of records based on multiple fields."""
        unique: List[Record] = []
        batch_records: List[Record] = []
        removed = 0

        for record in records:
            # 1. Exact match by URL hash
            h = url_hash(record.url or record.title)
            if h in self.seen_hashes:
                removed += 1
                continue

            is_duplicate = False
            for existing in batch_records:
                # 2. Heuristic duplicate check across fields
                # If titles are highly similar, it's a dupe
                t_sim = title_similarity(record.title, existing.title)

                # If titles are somewhat similar and it's the exact same date and source
                same_date = (
                    record.published_at
                    and existing.published_at
                    and (record.published_at[:10] == existing.published_at[:10])
                )
                same_source = record.source == existing.source

                # If descriptions are highly similar
                d_sim = (
                    text_similarity(record.description, existing.description)
                    if record.description and existing.description
                    else 0.0
                )

                if t_sim >= self.TITLE_SIMILARITY_THRESHOLD:
                    is_duplicate = True
                    break

                if d_sim >= self.DESC_SIMILARITY_THRESHOLD and t_sim > 0.6:
                    is_duplicate = True
                    break

                if t_sim > 0.7 and same_date and same_source:
                    is_duplicate = True
                    break

            if not is_duplicate:
                record.metadata["url_hash"] = h
                self.seen_hashes.add(h)
                batch_records.append(record)
                unique.append(record)
            else:
                removed += 1

        logger.info(
            f"Deduplicator: {len(unique)} unique, {removed} duplicates removed."
        )
        return unique
