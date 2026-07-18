"""
Preprocessor

Cleans and normalizes raw Record objects before NLP processing.

Responsibilities:
  - Strip HTML entities
  - Normalize Unicode
  - Filter non-English articles
  - Truncate to safe length
"""

import re
import html
from typing import List

from src.models.record import Record
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Characters from common European/Latin-script languages we can still process
_ASCII_THRESHOLD = 0.75  # If < 75% ASCII chars, skip as non-English


class Preprocessor:

    MAX_DESCRIPTION_LEN = 512

    def process(self, records: List[Record]) -> List[Record]:
        """
        Applies all cleaning steps to a list of records.
        Returns only valid, cleaned, English-language records.
        """
        cleaned = []
        skipped = 0

        for record in records:
            result = self._process_one(record)
            if result is not None:
                cleaned.append(result)
            else:
                skipped += 1

        logger.info(
            f"Preprocessor: {len(cleaned)} clean, {skipped} skipped."
        )
        return cleaned

    def _process_one(self, record: Record) -> Record | None:
        title = self._clean_text(record.title)
        description = self._clean_text(record.description or "")

        if not title:
            return None

        if not self._is_likely_english(title):
            return None

        # Return a new Record with cleaned fields (Records are dataclasses)
        record.title = title
        record.description = description[:self.MAX_DESCRIPTION_LEN]
        return record

    # ------------------------------------------------------------------
    # Text Cleaning
    # ------------------------------------------------------------------

    def _clean_text(self, text: str) -> str:
        """
        Strips HTML tags, decodes HTML entities, normalizes whitespace.
        """
        if not text:
            return ""

        # Decode HTML entities (&amp; → &, &#39; → ')
        text = html.unescape(text)

        # Remove HTML/XML tags
        text = re.sub(r"<[^>]+>", " ", text)

        # Collapse multiple spaces/newlines
        text = re.sub(r"\s+", " ", text).strip()

        return text

    # ------------------------------------------------------------------
    # Language Detection (lightweight heuristic — no extra dependency)
    # ------------------------------------------------------------------

    def _is_likely_english(self, text: str) -> bool:
        """
        Returns True if > 75% of characters are ASCII.
        This catches Hindi, Chinese, Arabic, etc. without langdetect overhead.
        """
        if not text:
            return False

        ascii_chars = sum(1 for c in text if ord(c) < 128)
        ratio = ascii_chars / len(text)
        return ratio >= _ASCII_THRESHOLD
