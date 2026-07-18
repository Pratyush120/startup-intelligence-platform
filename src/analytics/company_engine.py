"""
Strategic Decision Intelligence Platform

Company Intelligence Engine

Builds executive-level intelligence for every company.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from src.analytics.feature_engineering import CompanyFeatures
from src.analytics.scoring_engine import CompanyScore


# ==========================================================
# Company Intelligence Model
# ==========================================================

@dataclass
class CompanyIntelligence:

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    company_name: str

    # ------------------------------------------------------
    # Raw Event Metrics
    # ------------------------------------------------------

    total_events: int

    funding_events: int

    hiring_events: int

    layoff_events: int

    expansion_events: int

    acquisition_events: int

    total_funding: float

    average_confidence: float

    average_impact: float

    event_diversity: int

    source_diversity: int

    momentum: float

    latest_event: str

    latest_event_type: str

    latest_event_date: str

    # ------------------------------------------------------
    # Intelligence Scores
    # ------------------------------------------------------

    business_health: float

    growth_score: float

    investment_score: float

    influence_score: float

    risk_score: float

    confidence_grade: str

    recommendation: str

    score_breakdown: Dict[str, float]

    # ------------------------------------------------------
    # SWOT Intelligence
    # ------------------------------------------------------

    strengths: List[str]

    weaknesses: List[str]

    opportunities: List[str]

    threats: List[str]

    # ------------------------------------------------------
    # Executive Layer
    # ------------------------------------------------------

    executive_summary: str


# ==========================================================
# Company Engine
# ==========================================================

class CompanyEngine:

    """
    Converts engineered features and scores into complete
    company intelligence.
    """

    def build(

        self,

        features: CompanyFeatures,

        scores: CompanyScore

    ) -> CompanyIntelligence:

        strengths = []

        weaknesses = []

        opportunities = []

        threats = []

        # ==================================================
        # Strengths
        # ==================================================

        if features.funding_events:

            strengths.append(
                "Successfully attracted external investment."
            )

        if features.hiring_events:

            strengths.append(
                "Active hiring indicates business growth."
            )

        if features.expansion_events:

            strengths.append(
                "Expansion activities indicate scaling."
            )

        if features.average_confidence >= 0.90:

            strengths.append(
                "Business intelligence confidence is very high."
            )

        if features.event_diversity >= 3:

            strengths.append(
                "Company demonstrates diversified strategic activity."
            )

        # ==================================================
        # Weaknesses
        # ==================================================

        if features.layoff_events:

            weaknesses.append(
                "Layoff announcements increase operational uncertainty."
            )

        if features.event_diversity <= 1:

            weaknesses.append(
                "Limited strategic activity detected."
            )

        if features.average_confidence < 0.60:

            weaknesses.append(
                "Available intelligence has relatively low confidence."
            )

        # ==================================================
        # Opportunities
        # ==================================================

        if scores.growth_score >= 60:

            opportunities.append(
                "High growth opportunity."
            )

        if scores.investment_score >= 60:

            opportunities.append(
                "Attractive investment profile."
            )

        if scores.influence_score >= 50:

            opportunities.append(
                "Increasing market influence."
            )

        if features.source_diversity >= 2:

            opportunities.append(
                "Coverage across multiple independent news sources."
            )

        # ==================================================
        # Threats
        # ==================================================

        if scores.risk_score >= 50:

            threats.append(
                "Operational risk requires monitoring."
            )

        if features.layoff_events > 1:

            threats.append(
                "Repeated workforce reductions detected."
            )

        if scores.business_health < 40:

            threats.append(
                "Business health remains below healthy threshold."
            )

        # ==================================================
        # Executive Summary
        # ==================================================

        summary = self._summary(

            features,

            scores

        )

        return CompanyIntelligence(

            # Identity

            company_name=features.company_name,

            # Raw Metrics

            total_events=features.total_events,

            funding_events=features.funding_events,

            hiring_events=features.hiring_events,

            layoff_events=features.layoff_events,

            expansion_events=features.expansion_events,

            acquisition_events=features.acquisition_events,

            total_funding=features.total_funding,

            average_confidence=features.average_confidence,

            average_impact=features.average_impact,

            event_diversity=features.event_diversity,

            source_diversity=features.source_diversity,

            momentum=features.momentum,

            latest_event=features.latest_event,

            latest_event_type=features.latest_event_type,

            latest_event_date=features.latest_event_date,

            # Scores

            business_health=scores.business_health,

            growth_score=scores.growth_score,

            investment_score=scores.investment_score,

            influence_score=scores.influence_score,

            risk_score=scores.risk_score,

            confidence_grade=scores.confidence_grade,

            recommendation=scores.recommendation,

            score_breakdown=scores.breakdown,

            # SWOT

            strengths=strengths,

            weaknesses=weaknesses,

            opportunities=opportunities,

            threats=threats,

            # Executive

            executive_summary=summary

        )

    # ======================================================

    def _summary(

        self,

        features: CompanyFeatures,

        scores: CompanyScore

    ) -> str:

        lines = []

        lines.append(

            f"{features.company_name} generated "

            f"{features.total_events} strategic business events."

        )

        if features.funding_events:

            lines.append(

                "Funding activity reflects positive investor confidence."

            )

        if features.hiring_events:

            lines.append(

                "Hiring indicates organisational expansion."

            )

        if features.expansion_events:

            lines.append(

                "Expansion activity suggests market growth."

            )

        if features.acquisition_events:

            lines.append(

                "Acquisition activity strengthens strategic positioning."

            )

        if features.layoff_events:

            lines.append(

                "Layoff events increase operational risk."

            )

        lines.append(

            f"Overall Business Health Score is "

            f"{scores.business_health:.1f}/100."

        )

        lines.append(

            f"Current strategic recommendation: "

            f"{scores.recommendation}."

        )

        return " ".join(lines)