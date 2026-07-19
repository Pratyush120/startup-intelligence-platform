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


class LLMProvider(ABC):
    @abstractmethod
    def analyze(
        self, title: str, description: str, event_type: str, company: str
    ) -> LLMAnalysis:
        pass


class MockProvider(LLMProvider):
    def analyze(
        self, title: str, description: str, event_type: str, company: str
    ) -> LLMAnalysis:
        start = time.time()
        time.sleep(0.01)
        
        # Heuristic fallback when no LLM API key is present
        summary = description[:300] + "..." if len(description) > 300 else description
        if not summary:
            summary = title
            
        impact_keywords = ["revenue", "growth", "layoff", "acquire", "funding"]
        impact = f"Potential impact on {company}'s market trajectory."
        for kw in impact_keywords:
            if kw in description.lower():
                impact = f"Significant impact detected regarding {kw} for {company}."
                break

        return LLMAnalysis(
            executive_summary=summary,
            business_impact=impact,
            strategic_recommendation=f"Monitor {company} closely in the short term.",
            risk="Macroeconomic and execution risks.",
            opportunity="Market expansion and product innovation.",
            key_insight=f"Strategic developments for {company} are ongoing.",
            confidence=0.75,
            prompt_version="heuristic_v1",
            token_usage=0,
            processing_time_ms=int((time.time() - start) * 1000),
        )


class OpenAIProvider(LLMProvider):
    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=self._api_key)
        except ImportError:
            raise ImportError("openai package is required for OpenAIProvider")

    def analyze(
        self, title: str, description: str, event_type: str, company: str
    ) -> LLMAnalysis:
        start = time.time()
        safe_title = title[:200].replace("\n", " ")
        safe_desc = description[:400].replace("\n", " ")

        prompt = f"""You are a senior investment analyst. Analyze this startup news event.

Company: {company}
Event Type: {event_type}
Headline: {safe_title}
Details: {safe_desc}

Respond in this exact format (no markdown, one line per field):
SUMMARY: [1-2 sentence executive summary]
IMPACT: [1 sentence business impact]
RECOMMENDATION: [1 sentence strategic recommendation]
RISK: [1 sentence identifying key risk]
OPPORTUNITY: [1 sentence identifying key opportunity]
INSIGHT: [1 sentence key insight]
CONFIDENCE: [0.0-1.0 float]"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300,
            )
            text = response.choices[0].message.content or ""
            tokens = response.usage.total_tokens if response.usage else 0
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

        lines = {}
        for line in text.strip().split("\n"):
            if ":" in line:
                key, _, val = line.partition(":")
                lines[key.strip().upper()] = val.strip()

        try:
            confidence = float(lines.get("CONFIDENCE", "0.75"))
            confidence = max(0.0, min(1.0, confidence))
        except ValueError:
            confidence = 0.75

        return LLMAnalysis(
            executive_summary=lines.get("SUMMARY", "")[:300],
            business_impact=lines.get("IMPACT", "")[:200],
            strategic_recommendation=lines.get("RECOMMENDATION", "")[:200],
            risk=lines.get("RISK", "")[:200],
            opportunity=lines.get("OPPORTUNITY", "")[:200],
            key_insight=lines.get("INSIGHT", "")[:200],
            confidence=confidence,
            prompt_version="v1",
            token_usage=tokens,
            processing_time_ms=int((time.time() - start) * 1000),
        )


class LLMAnalyzer:
    def __init__(self, provider: Optional[LLMProvider] = None):
        if provider is None:
            if os.getenv("OPENAI_API_KEY"):
                try:
                    self.provider = OpenAIProvider()
                    logger.info("LLMAnalyzer: Initialized with OpenAIProvider")
                except Exception as e:
                    logger.warning(
                        f"Failed to init OpenAIProvider: {e}. Falling back to MockProvider"
                    )
                    self.provider = MockProvider()
            else:
                self.provider = MockProvider()
                logger.info(
                    "LLMAnalyzer: Initialized with MockProvider (No API key found)"
                )
        else:
            self.provider = provider

        self._cache: Dict[str, LLMAnalysis] = {}

    def analyze(
        self, title: str, description: str, event_type: str, company: str
    ) -> LLMAnalysis:
        cache_key = hashlib.md5(f"{title}:{event_type}".encode()).hexdigest()
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            result = self.provider.analyze(title, description, event_type, company)
            self._cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"LLM Provider {self.provider.__class__.__name__} failed: {e}")
            # Fallback to mock on failure
            mock = MockProvider()
            result = mock.analyze(title, description, event_type, company)
            self._cache[cache_key] = result
            return result
