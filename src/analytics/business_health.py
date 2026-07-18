"""
Business Health Score Engine

Computes an overall business health score for a company based on
detected business events.

This module contains no Streamlit code.
"""

from dataclasses import dataclass


@dataclass
class HealthResult:

    score: int

    status: str

    color: str

    breakdown: dict


class BusinessHealthEngine:

    WEIGHTS = {

        "Funding": 30,

        "Hiring": 20,

        "Expansion": 15,

        "Acquisition": 15,

        "Layoff": -20

    }

    def calculate(self, company: dict):

        score = 0

        breakdown = {}

        # ---------------- Funding ----------------

        funding = company.get("funding_events", 0)

        funding_score = min(funding * 30, 30)

        score += funding_score

        breakdown["Funding"] = funding_score

        # ---------------- Hiring ----------------

        hiring = company.get("hiring_events", 0)

        hiring_score = min(hiring * 20, 20)

        score += hiring_score

        breakdown["Hiring"] = hiring_score

        # ---------------- Expansion ----------------

        expansion = company.get("expansion_events", 0)

        expansion_score = min(expansion * 15, 15)

        score += expansion_score

        breakdown["Expansion"] = expansion_score

        # ---------------- Acquisition ----------------

        acquisition = company.get("acquisition_events", 0)

        acquisition_score = min(acquisition * 15, 15)

        score += acquisition_score

        breakdown["Acquisition"] = acquisition_score

        # ---------------- Layoffs ----------------

        layoffs = company.get("layoff_events", 0)

        layoff_penalty = layoffs * 20

        score -= layoff_penalty

        breakdown["Layoffs"] = -layoff_penalty

        # ---------------- Confidence ----------------

        confidence = company.get("average_confidence", 0.0)

        confidence_score = round(confidence * 10)

        score += confidence_score

        breakdown["Confidence"] = confidence_score

        # ---------------- Impact ----------------

        impact = company.get("average_impact", 0)

        impact_score = round(impact / 10)

        score += impact_score

        breakdown["Impact"] = impact_score

        # ---------------- Clamp ----------------

        score = max(0, min(score, 100))

        # ---------------- Status ----------------

        if score >= 80:

            status = "Excellent"

            color = "green"

        elif score >= 60:

            status = "Healthy"

            color = "blue"

        elif score >= 40:

            status = "Watch"

            color = "orange"

        else:

            status = "At Risk"

            color = "red"

        return HealthResult(

            score=score,

            status=status,

            color=color,

            breakdown=breakdown

        )