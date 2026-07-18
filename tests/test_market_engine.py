from src.analytics.market_engine import MarketEngine
from src.analytics.company_engine import CompanyIntelligence


def test_market_engine_build():
    companies = [
        CompanyIntelligence(
            company_name="CompanyA",
            total_events=10,
            funding_events=2,
            hiring_events=5,
            layoff_events=0,
            expansion_events=2,
            acquisition_events=1,
            total_funding=5000000.0,
            average_confidence=0.9,
            average_impact=0.8,
            event_diversity=5,
            source_diversity=3,
            momentum=50.0,
            latest_event="Acquired",
            latest_event_type="Acquisition",
            latest_event_date="2024-01-01",
            business_health=90.0,
            growth_score=85.0,
            investment_score=95.0,
            influence_score=80.0,
            risk_score=10.0,
            confidence_grade="A",
            recommendation="Invest",
            score_breakdown={},
            strengths=[],
            weaknesses=[],
            opportunities=[],
            threats=[],
            executive_summary="",
        ),
        CompanyIntelligence(
            company_name="CompanyB",
            total_events=5,
            funding_events=1,
            hiring_events=0,
            layoff_events=2,
            expansion_events=1,
            acquisition_events=1,
            total_funding=1000000.0,
            average_confidence=0.7,
            average_impact=0.6,
            event_diversity=3,
            source_diversity=2,
            momentum=20.0,
            latest_event="Layoffs",
            latest_event_type="Layoff",
            latest_event_date="2024-01-01",
            business_health=40.0,
            growth_score=50.0,
            investment_score=40.0,
            influence_score=30.0,
            risk_score=70.0,
            confidence_grade="C",
            recommendation="Monitor",
            score_breakdown={},
            strengths=[],
            weaknesses=[],
            opportunities=[],
            threats=[],
            executive_summary="",
        ),
    ]

    engine = MarketEngine()
    market = engine.build(companies)

    assert market.total_companies == 2
    assert market.total_events == 15
    assert market.total_funding == 6000000.0

    assert market.funding_events == 3
    assert market.hiring_events == 5
    assert market.layoff_events == 2

    assert market.average_business_health == 65.0
    assert market.average_growth_score == 67.5

    assert market.funding_share == 20.0  # 3/15
    assert market.hiring_share == 33.33  # 5/15

    assert market.top_company == "CompanyA"
    assert market.highest_risk_company == "CompanyB"

    assert market.market_health > 0
    assert market.investment_climate != ""
    assert market.growth_climate != ""
    assert market.risk_climate != ""

    assert market.market_concentration > 0

    # Empty case
    empty_market = engine.build([])
    assert empty_market.total_companies == 0
