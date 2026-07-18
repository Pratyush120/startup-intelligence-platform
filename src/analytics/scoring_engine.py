"""
Strategic Decision Intelligence Platform

Scoring Engine

Converts engineered company features into explainable
business intelligence scores.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from src.analytics.feature_engineering import CompanyFeatures


# ==========================================================
# Result Model
# ==========================================================


@dataclass
class CompanyScore:
    company_name: str

    business_health: float

    growth_score: float

    investment_score: float

    influence_score: float

    risk_score: float

    confidence_grade: str

    recommendation: str

    breakdown: Dict[str, float]


# ==========================================================
# Engine
# ==========================================================


class ScoringEngine:
    """
    Computes explainable business intelligence scores.
    """

    # ----------------------------
    # Adjustable Weights
    # ----------------------------

    FUNDING_WEIGHT = 30
    HIRING_WEIGHT = 20
    EXPANSION_WEIGHT = 15
    ACQUISITION_WEIGHT = 15

    CONFIDENCE_WEIGHT = 10
    IMPACT_WEIGHT = 10

    MOMENTUM_WEIGHT = 10

    DIVERSITY_WEIGHT = 5

    LAYOFF_PENALTY = 25

    # ------------------------------------------------------

    def score(self, features: CompanyFeatures) -> CompanyScore:

        breakdown = {}

        # ==================================================
        # Funding
        # ==================================================

        funding = min(features.funding_events * self.FUNDING_WEIGHT, 30)

        breakdown["Funding"] = funding

        # ==================================================
        # Hiring
        # ==================================================

        hiring = min(features.hiring_events * self.HIRING_WEIGHT, 20)

        breakdown["Hiring"] = hiring

        # ==================================================
        # Expansion
        # ==================================================

        expansion = min(features.expansion_events * self.EXPANSION_WEIGHT, 15)

        breakdown["Expansion"] = expansion

        # ==================================================
        # Acquisition
        # ==================================================

        acquisition = min(features.acquisition_events * self.ACQUISITION_WEIGHT, 15)

        breakdown["Acquisition"] = acquisition

        # ==================================================
        # Confidence
        # ==================================================

        confidence = round(features.average_confidence * self.CONFIDENCE_WEIGHT, 2)

        breakdown["Confidence"] = confidence

        # ==================================================
        # Impact
        # ==================================================

        impact = round(features.average_impact / 10, 2)

        breakdown["Impact"] = impact

        # ==================================================
        # Momentum
        # ==================================================

        momentum = min(features.momentum, self.MOMENTUM_WEIGHT)

        breakdown["Momentum"] = round(momentum, 2)

        # ==================================================
        # Diversity
        # ==================================================

        diversity = min(features.event_diversity, self.DIVERSITY_WEIGHT)

        breakdown["Diversity"] = diversity

        # ==================================================
        # Layoffs
        # ==================================================

        layoff_penalty = features.layoff_events * self.LAYOFF_PENALTY

        breakdown["Layoff Penalty"] = -layoff_penalty

        # ==================================================
        # Final Score
        # ==================================================

        business_health = (
            funding
            + hiring
            + expansion
            + acquisition
            + confidence
            + impact
            + momentum
            + diversity
            - layoff_penalty
        )

        business_health = max(0, min(round(business_health, 2), 100))

        # ==================================================
        # Growth Score
        # ==================================================

        growth = funding + hiring + expansion

        growth = min(growth, 100)

        # ==================================================
        # Investment Score
        # ==================================================

        investment = funding + confidence + impact

        investment = min(investment, 100)

        # ==================================================
        # Influence
        # ==================================================

        influence = min(features.total_events * 10, 100)

        # ==================================================
        # Risk
        # ==================================================

        risk = min(layoff_penalty + max(0, 5 - features.event_diversity) * 5, 100)

        # ==================================================
        # Confidence Grade
        # ==================================================

        avg = features.average_confidence

        if avg >= 0.90:
            grade = "A+"

        elif avg >= 0.80:
            grade = "A"

        elif avg >= 0.70:
            grade = "B"

        elif avg >= 0.60:
            grade = "C"

        else:
            grade = "D"

        # ==================================================
        # Recommendation
        # ==================================================

        if business_health >= 85:
            recommendation = "Strong Buy"

        elif business_health >= 70:
            recommendation = "Buy"

        elif business_health >= 55:
            recommendation = "Watch"

        elif business_health >= 40:
            recommendation = "Neutral"

        else:
            recommendation = "High Risk"

        # ==================================================

        return CompanyScore(
            company_name=features.company_name,
            business_health=business_health,
            growth_score=round(growth, 2),
            investment_score=round(investment, 2),
            influence_score=round(influence, 2),
            risk_score=round(risk, 2),
            confidence_grade=grade,
            recommendation=recommendation,
            breakdown=breakdown,
        )
