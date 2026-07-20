"""
LLM Analyzer

Generates AI-powered strategic summaries and confidence scores.
"""

from __future__ import annotations

import time
import hashlib
from typing import Dict

from src.services.providers.gemini_provider import GeminiProvider, EventAnalysisResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LLMAnalyzer:
    def __init__(self):
        self.provider = GeminiProvider()
        self._cache: Dict[str, EventAnalysisResponse] = {}

    def analyze(self, title: str, description: str, event_type: str, company: str):
        cache_key = hashlib.md5(f"{title}:{event_type}:{company}".encode()).hexdigest()
        if cache_key in self._cache:
            return self._cache[cache_key]

        start = time.time()

        try:
            result = self.provider.analyze_event(
                title, description, event_type, company
            )
            result.processing_time_ms = int((time.time() - start) * 1000)
            self._cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"Gemini LLM Analyzer failed: {e}")
            raise RuntimeError(f"Pipeline analysis failed: {e}")
