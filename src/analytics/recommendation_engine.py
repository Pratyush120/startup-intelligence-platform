"""
Strategic Decision Intelligence Platform

Recommendation Engine

Generates explainable strategic recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.analytics.company_engine import CompanyIntelligence


# ==========================================================
# Recommendation Model
# ==========================================================


@dataclass
class CompanyRecommendation:
    company_name: str

    recommendation: str

    confidence: str

    priority: int

    rationale: List[str] = field(default_factory=list)

    actions: List[str] = field(default_factory=list)


# ==========================================================
# Recommendation Engine
# ==========================================================


class RecommendationEngine:
    """
    Generates strategic recommendations for companies.
    """

    def recommend(self, company: CompanyIntelligence) -> CompanyRecommendation:

        rationale = []

        actions = []

        score = company.business_health

        # -----------------------------------------

        if score >= 85:
            recommendation = "Strong Buy"

            priority = 1

        elif score >= 70:
            recommendation = "Buy"

            priority = 2

        elif score >= 55:
            recommendation = "Watch"

            priority = 3

        else:
            recommendation = "High Risk"

            priority = 4

        # -----------------------------------------
        # Rationale
        # -----------------------------------------

        if company.funding_events:
            rationale.append("Recent funding demonstrates investor confidence.")

        if company.hiring_events:
            rationale.append("Hiring activity indicates business expansion.")

        if company.expansion_events:
            rationale.append("Expansion signals long-term growth.")

        if company.acquisition_events:
            rationale.append("Acquisition activity strengthens market position.")

        if company.layoff_events:
            rationale.append("Layoff announcements increase operational risk.")

        if company.average_confidence >= 0.90:
            rationale.append("High confidence business intelligence.")

        # -----------------------------------------
        # Suggested Actions
        # -----------------------------------------

        if recommendation == "Strong Buy":
            actions.extend(
                [
                    "Monitor future funding rounds.",
                    "Track hiring momentum.",
                    "Evaluate long-term partnerships.",
                ]
            )

        elif recommendation == "Buy":
            actions.extend(
                [
                    "Continue monitoring quarterly developments.",
                    "Watch for expansion announcements.",
                ]
            )

        elif recommendation == "Watch":
            actions.extend(
                ["Observe funding momentum.", "Monitor business health changes."]
            )

        else:
            actions.extend(
                ["Investigate operational risks.", "Track restructuring activities."]
            )

        # -----------------------------------------
        # Confidence
        # -----------------------------------------

        if company.average_confidence >= 0.90:
            confidence = "Very High"

        elif company.average_confidence >= 0.80:
            confidence = "High"

        elif company.average_confidence >= 0.70:
            confidence = "Medium"

        else:
            confidence = "Low"

        return CompanyRecommendation(
            company_name=company.company_name,
            recommendation=recommendation,
            confidence=confidence,
            priority=priority,
            rationale=rationale,
            actions=actions,
        )
