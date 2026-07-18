"""
Strategic Decision Intelligence Platform

Market Intelligence Engine

Aggregates company-level intelligence into ecosystem-wide
market intelligence.

This module contains no UI code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict

from src.analytics.company_engine import CompanyIntelligence


# ==========================================================
# Market Intelligence Model
# ==========================================================

@dataclass
class MarketIntelligence:
    """
    Executive view of the startup ecosystem.
    """

    # -----------------------------------------
    # Ecosystem Size
    # -----------------------------------------

    total_companies: int = 0

    total_events: int = 0

    total_funding: float = 0.0

    # -----------------------------------------
    # Event Totals
    # -----------------------------------------

    funding_events: int = 0

    hiring_events: int = 0

    layoff_events: int = 0

    expansion_events: int = 0

    acquisition_events: int = 0

    # -----------------------------------------
    # Average Scores
    # -----------------------------------------

    average_business_health: float = 0.0

    average_growth_score: float = 0.0

    average_investment_score: float = 0.0

    average_risk_score: float = 0.0

    average_confidence: float = 0.0

    # -----------------------------------------
    # Market Shares
    # -----------------------------------------

    funding_share: float = 0.0

    hiring_share: float = 0.0

    expansion_share: float = 0.0

    layoff_share: float = 0.0

    acquisition_share: float = 0.0

    # -----------------------------------------
    # Market Leaders
    # -----------------------------------------

    top_company: str = ""

    top_growth_company: str = ""

    highest_risk_company: str = ""

    highest_investment_company: str = ""

    most_influential_company: str = ""

    # -----------------------------------------
    # Concentration
    # -----------------------------------------

    market_concentration: float = 0.0

    # -----------------------------------------
    # Intelligence
    # -----------------------------------------

    market_sentiment: str = ""

    investment_climate: str = ""

    growth_climate: str = ""

    risk_climate: str = ""

    dominant_activity: str = ""

    # -----------------------------------------
    # Explainability
    # -----------------------------------------

    insights: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)


# ==========================================================
# Market Engine
# ==========================================================

class MarketEngine:
    """
    Aggregates company intelligence into market intelligence.
    """

    def build(
        self,
        companies: List[CompanyIntelligence]
    ) -> MarketIntelligence:

        market = MarketIntelligence()

        if not companies:
            return market

        market.total_companies = len(companies)

        self._aggregate_metrics(
            market,
            companies
        )

        self._calculate_market_shares(
            market
        )

        self._identify_market_leaders(
            market,
            companies
        )

        self._build_market_state(
        market
        )

        self._finalize(
        market
        )


        return market

    # ======================================================
    # Aggregation
    # ======================================================

    def _aggregate_metrics(
        self,
        market: MarketIntelligence,
        companies: List[CompanyIntelligence]
    ):

        """
        Aggregate raw metrics across all companies.
        """

        for company in companies:

            market.total_events += company.total_events

            market.total_funding += company.total_funding

            market.funding_events += company.funding_events

            market.hiring_events += company.hiring_events

            market.layoff_events += company.layoff_events

            market.expansion_events += company.expansion_events

            market.acquisition_events += company.acquisition_events

            market.average_business_health += company.business_health

            market.average_growth_score += company.growth_score

            market.average_investment_score += company.investment_score

            market.average_risk_score += company.risk_score

            market.average_confidence += company.average_confidence

        count = market.total_companies

        market.average_business_health /= count

        market.average_growth_score /= count

        market.average_investment_score /= count

        market.average_risk_score /= count

        market.average_confidence /= count

            # ======================================================
    # Market Share Calculation
    # ======================================================

    def _calculate_market_shares(
        self,
        market: MarketIntelligence
    ):
        """
        Calculate percentage share of each business activity.
        """

        total = (
            market.funding_events
            + market.hiring_events
            + market.layoff_events
            + market.expansion_events
            + market.acquisition_events
        )

        if total == 0:
            return

        market.funding_share = round(
            market.funding_events * 100 / total, 2
        )

        market.hiring_share = round(
            market.hiring_events * 100 / total, 2
        )

        market.expansion_share = round(
            market.expansion_events * 100 / total, 2
        )

        market.layoff_share = round(
            market.layoff_events * 100 / total, 2
        )

        market.acquisition_share = round(
            market.acquisition_events * 100 / total, 2
        )


    # ======================================================
    # Market Leaders
    # ======================================================

    def _identify_market_leaders(
        self,
        market: MarketIntelligence,
        companies: List[CompanyIntelligence]
    ):
        """
        Identify leaders across different business dimensions.
        """

        # --------------------------------------------------

        market.top_company = max(
            companies,
            key=lambda c: c.business_health
        ).company_name

        market.top_growth_company = max(
            companies,
            key=lambda c: c.growth_score
        ).company_name

        market.highest_investment_company = max(
            companies,
            key=lambda c: c.investment_score
        ).company_name

        market.highest_risk_company = max(
            companies,
            key=lambda c: c.risk_score
        ).company_name

        market.most_influential_company = max(
            companies,
            key=lambda c: c.influence_score
        ).company_name

        # --------------------------------------------------

        self._calculate_market_concentration(
            market,
            companies
        )


    # ======================================================
    # Market Concentration (HHI)
    # ======================================================

    def _calculate_market_concentration(
        self,
        market: MarketIntelligence,
        companies: List[CompanyIntelligence]
    ):
        """
        Computes an HHI-like concentration score using
        total funding distribution.

        HHI:
            <1500      Competitive
            1500-2500  Moderate
            >2500      Highly Concentrated
        """

        total = sum(
            c.total_funding
            for c in companies
        )

        if total == 0:

            market.market_concentration = 0

            return

        hhi = 0

        for company in companies:

            share = company.total_funding / total

            hhi += (share * 100) ** 2

        market.market_concentration = round(
            hhi,
            2
        )


    # ======================================================
    # Dominant Market Activity
    # ======================================================

    def _dominant_activity(
        self,
        market: MarketIntelligence
    ):

        values = {

            "Funding": market.funding_events,

            "Hiring": market.hiring_events,

            "Expansion": market.expansion_events,

            "Layoff": market.layoff_events,

            "Acquisition": market.acquisition_events

        }

        market.dominant_activity = max(
            values,
            key=values.get
        )


    # ======================================================
    # Funding Distribution
    # ======================================================

    def top_funding_companies(
        self,
        companies: List[CompanyIntelligence],
        limit: int = 10
    ):
        """
        Returns companies sorted by funding amount.
        """

        return sorted(

            companies,

            key=lambda c: c.total_funding,

            reverse=True

        )[:limit]


    # ======================================================
    # Business Health Ranking
    # ======================================================

    def healthiest_companies(
        self,
        companies: List[CompanyIntelligence],
        limit: int = 10
    ):

        return sorted(

            companies,

            key=lambda c: c.business_health,

            reverse=True

        )[:limit]


    # ======================================================
    # Highest Growth Ranking
    # ======================================================

    def fastest_growing(
        self,
        companies: List[CompanyIntelligence],
        limit: int = 10
    ):

        return sorted(

            companies,

            key=lambda c: c.growth_score,

            reverse=True

        )[:limit]


    # ======================================================
    # Highest Risk Ranking
    # ======================================================

    def highest_risk(
        self,
        companies: List[CompanyIntelligence],
        limit: int = 10
    ):

        return sorted(

            companies,

            key=lambda c: c.risk_score,

            reverse=True

        )[:limit]
        # ======================================================
    # Ecosystem Health Index
    # ======================================================

    def _ecosystem_health_score(
        self,
        market: MarketIntelligence
    ) -> float:
        """
        Computes an overall ecosystem health score (0-100).

        Components:
            Business Health       35%
            Growth                25%
            Investment            20%
            Confidence            10%
            Risk                  10% (negative)
        """

        score = (
            market.average_business_health * 0.35
            + market.average_growth_score * 0.25
            + market.average_investment_score * 0.20
            + (market.average_confidence * 100) * 0.10
            + (100 - market.average_risk_score) * 0.10
        )

        return round(

            min(max(score, 0), 100),

            2

        )

    # ======================================================
    # Market Sentiment
    # ======================================================

    def _market_sentiment(
        self,
        score: float
    ) -> str:

        if score >= 85:
            return "Very Positive"

        if score >= 70:
            return "Positive"

        if score >= 55:
            return "Stable"

        if score >= 40:
            return "Weak"

        return "Negative"

    # ======================================================
    # Investment Climate
    # ======================================================

    def _investment_climate(
        self,
        market: MarketIntelligence
    ) -> str:

        investment = market.average_investment_score

        if investment >= 80:
            return "Excellent"

        if investment >= 65:
            return "Healthy"

        if investment >= 50:
            return "Moderate"

        if investment >= 35:
            return "Weak"

        return "Poor"

    # ======================================================
    # Growth Climate
    # ======================================================

    def _growth_climate(
        self,
        market: MarketIntelligence
    ) -> str:

        growth = market.average_growth_score

        if growth >= 80:
            return "Hyper Growth"

        if growth >= 60:
            return "High Growth"

        if growth >= 45:
            return "Growing"

        if growth >= 30:
            return "Stable"

        return "Slow"

    # ======================================================
    # Risk Climate
    # ======================================================

    def _risk_climate(
        self,
        market: MarketIntelligence
    ) -> str:

        risk = market.average_risk_score

        if risk >= 75:
            return "Critical"

        if risk >= 55:
            return "High"

        if risk >= 35:
            return "Moderate"

        return "Low"

    # ======================================================
    # Build Market Intelligence
    # ======================================================

    def _build_market_state(
        self,
        market: MarketIntelligence
    ):
        """
        Populate high-level market intelligence.
        """

        ecosystem = self._ecosystem_health_score(
            market
        )

        market.market_sentiment = self._market_sentiment(
            ecosystem
        )
        
        market_health: float = 0.0
        market.market_health = round(
            ecosystem,
            2
        )

        market.investment_climate = self._investment_climate(
            market
        )

        market.growth_climate = self._growth_climate(
            market
        )

        market.risk_climate = self._risk_climate(
            market
        )

        self._dominant_activity(
            market
        )
        