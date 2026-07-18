"""
Strategic Trend Engine

Analyses the overall startup ecosystem and detects
strategic market trends.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.analytics.market_engine import MarketIntelligence


# ==========================================================
# Trend Model
# ==========================================================

@dataclass
class TrendReport:

    market_phase: str

    investment_outlook: str

    growth_outlook: str

    risk_outlook: str

    dominant_strategy: str

    emerging_signal: str

    market_summary: str

    opportunities: List[str] = field(default_factory=list)

    risks: List[str] = field(default_factory=list)

    observations: List[str] = field(default_factory=list)


# ==========================================================
# Trend Engine
# ==========================================================

class TrendEngine:

    """
    Produces strategic trends from market intelligence.
    """

    def analyse(
        self,
        market: MarketIntelligence
    ) -> TrendReport:

        opportunities = []

        risks = []

        observations = []

        # --------------------------------------------
        # Market Phase
        # --------------------------------------------

        if market.market_health >= 80:

            phase = "Expansion"

        elif market.market_health >= 60:

            phase = "Growth"

        elif market.market_health >= 40:

            phase = "Stable"

        else:

            phase = "Contraction"

        # --------------------------------------------
        # Investment Outlook
        # --------------------------------------------

        investment = market.investment_climate

        # --------------------------------------------
        # Growth Outlook
        # --------------------------------------------

        growth = market.growth_climate

        # --------------------------------------------
        # Risk Outlook
        # --------------------------------------------

        risk = market.risk_climate

        # --------------------------------------------
        # Dominant Strategy
        # --------------------------------------------

        dominant = market.dominant_activity

        # --------------------------------------------
        # Emerging Signal
        # --------------------------------------------

        if market.funding_share >= 50:

            emerging = "Funding-led ecosystem"

        elif market.hiring_share >= 25:

            emerging = "Hiring acceleration"

        elif market.expansion_share >= 20:

            emerging = "Rapid market expansion"

        elif market.layoff_share >= 20:

            emerging = "Operational restructuring"

        else:

            emerging = "Balanced ecosystem"

        # --------------------------------------------
        # Opportunities
        # --------------------------------------------

        if market.market_health >= 75:

            opportunities.append(

                "Overall business environment is healthy."

            )

        if market.investment_climate in (

            "Excellent",

            "Healthy"

        ):

            opportunities.append(

                "Investment climate is favourable."

            )

        if market.growth_climate in (

            "High Growth",

            "Hyper Growth"

        ):

            opportunities.append(

                "Growth momentum remains strong."

            )

        if market.market_concentration < 1500:

            opportunities.append(

                "Capital distribution is well diversified."

            )

        # --------------------------------------------
        # Risks
        # --------------------------------------------

        if market.risk_climate == "Critical":

            risks.append(

                "Market-wide operational risk is elevated."

            )

        if market.market_concentration >= 2500:

            risks.append(

                "Funding is concentrated in very few companies."

            )

        if market.layoff_share >= 15:

            risks.append(

                "Layoff activity is increasing."

            )

        # --------------------------------------------
        # Observations
        # --------------------------------------------

        observations.append(

            f"Funding contributes {market.funding_share:.1f}% "

            f"of all detected business activity."

        )

        observations.append(

            f"Average ecosystem health is "

            f"{market.market_health:.1f}/100."

        )

        observations.append(

            f"The strongest company is "

            f"{market.top_company}."

        )

        observations.append(

            f"The fastest growing company is "

            f"{market.top_growth_company}."

        )

        observations.append(

            f"The dominant ecosystem activity is "

            f"{market.dominant_activity.lower()}."

        )

        # --------------------------------------------
        # Summary
        # --------------------------------------------

        summary = (

            f"The startup ecosystem is currently in a "

            f"{phase.lower()} phase with "

            f"{investment.lower()} investment conditions "

            f"and {growth.lower()} growth prospects."

        )

        return TrendReport(

            market_phase=phase,

            investment_outlook=investment,

            growth_outlook=growth,

            risk_outlook=risk,

            dominant_strategy=dominant,

            emerging_signal=emerging,

            market_summary=summary,

            opportunities=opportunities,

            risks=risks,

            observations=observations

        )