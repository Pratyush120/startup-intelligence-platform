"""
LLM Analyzer

Generates AI-powered strategic summaries and confidence scores.
"""

from __future__ import annotations

import time
import hashlib
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class LLMAnalysis:
    executive_summary: str = ""
    business_impact: str = ""
    strategic_recommendation: str = ""
    risk: str = ""
    opportunity: str = ""
    key_insight: str = ""
    confidence: float = 0.75
    prompt_version: str = "v1"
    token_usage: int = 0
    processing_time_ms: int = 0


import time
import hashlib
from typing import Dict
from src.utils.logger import get_logger
from src.services.providers.gemini_provider import GeminiProvider, EventAnalysisResponse

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
            result = self.provider.analyze_event(title, description, event_type, company)
            result.processing_time_ms = int((time.time() - start) * 1000)
            self._cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"Gemini LLM Analyzer failed: {e}")
            raise RuntimeError(f"Pipeline analysis failed: {e}")
