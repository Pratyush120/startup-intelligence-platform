"""
LLM Analyzer

Generates AI-powered strategic summaries and confidence scores.

Design:
  - Primary:  OpenAI GPT-4o-mini or Google Gemini
  - Fallback: Rule-based summarizer (no API key required)
  - Cache:    In-memory dict keyed by title hash to avoid re-analysis
  - Budget:   MAX_LLM_CALLS_PER_RUN caps API spend
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)

MAX_LLM_CALLS_PER_RUN = int(os.getenv("MAX_LLM_CALLS", "100"))


@dataclass
class LLMAnalysis:
    ai_summary: str = ""
    business_impact: str = ""
    confidence: float = 0.75
    risk_tags: List[str] = field(default_factory=list)
    opportunity_tags: List[str] = field(default_factory=list)


_IMPACT_TEMPLATES: dict[str, str] = {
    "Funding": "Signals investor confidence and accelerates growth runway.",
    "Acquisition": "Consolidates market position and expands product capabilities.",
    "Hiring": "Indicates business expansion and operational scaling.",
    "Layoff": "Raises operational risk and may signal financial stress.",
    "IPO": "Creates liquidity event and increases public market scrutiny.",
    "Product Launch": "Expands addressable market and increases competitive pressure.",
    "Partnership": "Strengthens ecosystem ties and opens new distribution channels.",
    "Expansion": "Demonstrates geographic or vertical growth ambition.",
    "Litigation": "Introduces regulatory and financial risk to the business.",
    "Leadership": "Signals strategic direction change at the executive level.",
    "General": "Represents a notable development in the company trajectory.",
}

_RISK_TAGS: dict[str, List[str]] = {
    "Layoff": ["workforce_reduction", "financial_stress"],
    "Litigation": ["regulatory_risk", "legal_exposure"],
    "Acquisition": ["integration_risk"],
}

_OPPORTUNITY_TAGS: dict[str, List[str]] = {
    "Funding": ["growth_capital", "expansion_ready"],
    "Acquisition": ["market_consolidation", "capability_expansion"],
    "IPO": ["liquidity_event", "public_market_access"],
    "Partnership": ["distribution_growth", "ecosystem_expansion"],
    "Product Launch": ["market_expansion", "competitive_differentiation"],
    "Hiring": ["scale_signal"],
    "Expansion": ["geographic_growth"],
}


def _rule_based_analysis(title: str, event_type: str, company: str) -> LLMAnalysis:
    impact = _IMPACT_TEMPLATES.get(event_type, _IMPACT_TEMPLATES["General"])
    summary = f"{company}: {title.strip().rstrip('.')}. {impact}"
    return LLMAnalysis(
        ai_summary=summary[:300],
        business_impact=impact,
        confidence=0.70,
        risk_tags=_RISK_TAGS.get(event_type, []),
        opportunity_tags=_OPPORTUNITY_TAGS.get(event_type, []),
    )


class LLMAnalyzer:

    def __init__(self):
        self._openai_key = os.getenv("OPENAI_API_KEY")
        self._gemini_key = os.getenv("GOOGLE_API_KEY")
        self._cache: Dict[str, LLMAnalysis] = {}
        self._call_count = 0

        if self._openai_key:
            logger.info("LLMAnalyzer: OpenAI mode enabled.")
        elif self._gemini_key:
            logger.info("LLMAnalyzer: Gemini mode enabled.")
        else:
            logger.warning("LLMAnalyzer: No API key. Rule-based fallback.")

    def analyze(
        self,
        title: str,
        description: str,
        event_type: str,
        company: str,
    ) -> LLMAnalysis:
        # Cache check
        cache_key = hashlib.md5(f"{title}:{event_type}".encode()).hexdigest()
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Budget check
        if self._call_count >= MAX_LLM_CALLS_PER_RUN:
            logger.info(f"LLM budget exhausted ({MAX_LLM_CALLS_PER_RUN}). Using fallback.")
            result = _rule_based_analysis(title, event_type, company)
            self._cache[cache_key] = result
            return result

        # Try LLM providers
        if self._openai_key:
            try:
                result = self._openai_analyze(title, description, event_type, company)
                self._call_count += 1
                self._cache[cache_key] = result
                return result
            except Exception as e:
                logger.warning(f"OpenAI call failed: {e}. Using fallback.")

        if self._gemini_key:
            try:
                result = self._gemini_analyze(title, description, event_type, company)
                self._call_count += 1
                self._cache[cache_key] = result
                return result
            except Exception as e:
                logger.warning(f"Gemini call failed: {e}. Using fallback.")

        result = _rule_based_analysis(title, event_type, company)
        self._cache[cache_key] = result
        return result

    def _openai_analyze(self, title: str, description: str, event_type: str, company: str) -> LLMAnalysis:
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=self._openai_key)
        prompt = self._build_prompt(title, description, event_type, company)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
        )
        return self._parse_response(response.choices[0].message.content or "", event_type)

    def _gemini_analyze(self, title: str, description: str, event_type: str, company: str) -> LLMAnalysis:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=self._gemini_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = self._build_prompt(title, description, event_type, company)
        response = model.generate_content(prompt)
        return self._parse_response(response.text or "", event_type)

    def _build_prompt(self, title: str, description: str, event_type: str, company: str) -> str:
        # Sanitize inputs to prevent prompt injection
        safe_title = title[:200].replace('\n', ' ')
        safe_desc = description[:400].replace('\n', ' ')
        return f"""You are a senior investment analyst. Analyze this startup news event.

Company: {company}
Event Type: {event_type}
Headline: {safe_title}
Details: {safe_desc}

Respond in this exact format (no markdown):
SUMMARY: [1-2 sentence executive summary, max 200 chars]
IMPACT: [1 sentence business impact]
CONFIDENCE: [0.0-1.0 float]
RISK_TAGS: [comma-separated tags]
OPPORTUNITY_TAGS: [comma-separated tags]"""

    def _parse_response(self, text: str, event_type: str) -> LLMAnalysis:
        lines: dict[str, str] = {}
        for line in text.strip().split("\n"):
            if ":" in line:
                key, _, val = line.partition(":")
                lines[key.strip().upper()] = val.strip()

        try:
            confidence = float(lines.get("CONFIDENCE", "0.75"))
            confidence = max(0.0, min(1.0, confidence))
        except ValueError:
            confidence = 0.75

        def parse_tags(raw: str) -> List[str]:
            if not raw:
                return []
            return [t.strip() for t in raw.split(",") if t.strip()]

        return LLMAnalysis(
            ai_summary=lines.get("SUMMARY", "")[:300],
            business_impact=lines.get("IMPACT", ""),
            confidence=confidence,
            risk_tags=parse_tags(lines.get("RISK_TAGS", "")),
            opportunity_tags=parse_tags(lines.get("OPPORTUNITY_TAGS", "")),
        )
