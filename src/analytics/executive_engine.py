"""
Strategic Decision Intelligence Platform

Executive Intelligence Engine

Generates executive-ready intelligence from the
market and trend engines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.analytics.market_engine import MarketIntelligence
from src.analytics.trend_engine import TrendReport


# ==========================================================
# Executive Brief
# ==========================================================


@dataclass
class ExecutiveBrief:
    title: str

    overview: str

    ecosystem_health: str

    investment_outlook: str

    growth_outlook: str

    risk_outlook: str

    dominant_strategy: str

    key_insights: List[str] = field(default_factory=list)

    strategic_actions: List[str] = field(default_factory=list)

    business_risks: List[str] = field(default_factory=list)

    confidence_statement: str = ""

    conclusion: str = ""


# ==========================================================
# Executive Engine
# ==========================================================


class ExecutiveEngine:
    """
    Generates an executive-level intelligence report.
    """

    def generate(
        self, market: MarketIntelligence, trend: TrendReport
    ) -> ExecutiveBrief:

        # ----------------------------------------------

        overview = (
            f"The platform analysed "
            f"{market.total_companies} companies "
            f"across {market.total_events} strategic "
            f"business events."
        )

        # ----------------------------------------------

        ecosystem = (
            f"Ecosystem Health : "
            f"{market.market_health:.1f}/100 "
            f"({market.market_sentiment})"
        )

        # ----------------------------------------------

        insights = []

        insights.append(
            f"Funding contributes {market.funding_share:.1f}% of ecosystem activity."
        )

        insights.append(f"Top performing company: {market.top_company}")

        insights.append(f"Fastest growing company: {market.top_growth_company}")

        insights.append(
            f"Highest investment attractiveness: {market.highest_investment_company}"
        )

        insights.append(f"Dominant business activity: {market.dominant_activity}")

        # ----------------------------------------------

        actions = []

        if market.market_health >= 80:
            actions.append("Accelerate strategic investment activities.")

        elif market.market_health >= 60:
            actions.append("Continue selective investment in high-growth companies.")

        else:
            actions.append("Adopt a conservative investment strategy.")

        if market.market_concentration >= 2500:
            actions.append("Diversify investment across emerging companies.")

        if market.growth_climate in ("Hyper Growth", "High Growth"):
            actions.append("Increase focus on rapidly scaling businesses.")

        if market.risk_climate in ("Critical", "High"):
            actions.append("Strengthen operational risk monitoring.")

        # ----------------------------------------------

        risks = []

        risks.extend(trend.risks)

        risks.extend(market.warnings)

        # ----------------------------------------------

        confidence = (
            f"Average intelligence confidence is {market.average_confidence:.2f}."
        )

        # ----------------------------------------------

        conclusion = (
            f"The ecosystem is currently in a "
            f"{trend.market_phase.lower()} phase "
            f"with {market.market_sentiment.lower()} "
            f"market sentiment. "
            f"The dominant strategic activity "
            f"continues to be "
            f"{market.dominant_activity.lower()}."
        )

        # ----------------------------------------------

        return ExecutiveBrief(
            title="Executive Intelligence Brief",
            overview=overview,
            ecosystem_health=ecosystem,
            investment_outlook=trend.investment_outlook,
            growth_outlook=trend.growth_outlook,
            risk_outlook=trend.risk_outlook,
            dominant_strategy=trend.dominant_strategy,
            key_insights=insights,
            strategic_actions=actions,
            business_risks=risks,
            confidence_statement=confidence,
            conclusion=conclusion,
        )
