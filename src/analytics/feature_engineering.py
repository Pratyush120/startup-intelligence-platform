"""
Feature Engineering Engine

Transforms raw business events into structured company features.

This is the foundation of the intelligence layer.

No UI.
No Database.
Pure business analytics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import Counter
from typing import Dict, List

from src.models.events.business_event import BusinessEvent


# ==========================================================
# Feature Model
# ==========================================================

@dataclass
class CompanyFeatures:

    company_name: str

    total_events: int = 0

    funding_events: int = 0

    hiring_events: int = 0

    layoff_events: int = 0

    expansion_events: int = 0

    acquisition_events: int = 0

    total_funding: float = 0

    average_confidence: float = 0

    average_impact: float = 0

    event_diversity: int = 0

    source_diversity: int = 0

    momentum: float = 0

    latest_event: str | None = None

    latest_event_type: str | None = None

    latest_event_date: str | None = None

    event_counter: Dict[str, int] = field(default_factory=dict)

    sources: List[str] = field(default_factory=list)


# ==========================================================
# Feature Engineering Engine
# ==========================================================

class FeatureEngineeringEngine:

    """
    Converts BusinessEvents into company-level features.
    """

    def build(self, events: List[BusinessEvent]) -> Dict[str, CompanyFeatures]:

        companies: Dict[str, CompanyFeatures] = {}

        for event in events:

            if not event.company:
                continue

            company = event.company

            if company not in companies:

                companies[company] = CompanyFeatures(

                    company_name=company

                )

            features = companies[company]

            # ----------------------------------

            features.total_events += 1

            # ----------------------------------

            if event.event_type == "Funding":

                features.funding_events += 1

                amount = event.entities.get("amount")

                if amount:

                    try:

                        features.total_funding += float(amount)

                    except:

                        pass

            elif event.event_type == "Hiring":

                features.hiring_events += 1

            elif event.event_type == "Layoff":

                features.layoff_events += 1

            elif event.event_type == "Expansion":

                features.expansion_events += 1

            elif event.event_type == "Acquisition":

                features.acquisition_events += 1

            # ----------------------------------

            features.average_confidence += event.confidence

            features.average_impact += event.impact_score

            # ----------------------------------

            features.sources.append(event.source)

            # ----------------------------------

            features.latest_event = event.title

            features.latest_event_type = event.event_type

            features.latest_event_date = event.published_at

            # ----------------------------------

            features.event_counter[event.event_type] = (

                features.event_counter.get(

                    event.event_type,

                    0

                )

                + 1

            )

        # =====================================================

        for feature in companies.values():

            if feature.total_events:

                feature.average_confidence /= feature.total_events

                feature.average_impact /= feature.total_events

            feature.source_diversity = len(

                set(feature.sources)

            )

            feature.event_diversity = len(

                feature.event_counter

            )

            feature.momentum = (

                feature.total_events

                * feature.average_confidence

                * (1 + feature.event_diversity * 0.10)

            )

        return companies