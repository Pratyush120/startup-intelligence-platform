from src.analytics.company_engine import CompanyEngine
from src.analytics.feature_engineering import CompanyFeatures
from src.analytics.scoring_engine import CompanyScore


def test_company_engine_build():
    features = CompanyFeatures(
        company_name="TestCompany",
        total_events=5,
        funding_events=1,
        hiring_events=1,
        layoff_events=1,
        expansion_events=1,
        acquisition_events=1,
        total_funding=1000000.0,
        average_confidence=0.9,
        average_impact=0.8,
        event_diversity=5,
        source_diversity=3,
        momentum=10.0,
        latest_event="Acquired",
        latest_event_type="Acquisition",
        latest_event_date="2024-01-01",
    )

    scores = CompanyScore(
        company_name="TestCompany",
        business_health=85.0,
        growth_score=90.0,
        investment_score=80.0,
        influence_score=60.0,
        risk_score=20.0,
        confidence_grade="A",
        recommendation="Invest",
        breakdown={},
    )

    engine = CompanyEngine()
    intel = engine.build(features, scores)

    assert intel.company_name == "TestCompany"
    assert intel.business_health == 85.0
    assert "Successfully attracted external investment." in intel.strengths
    assert "Active hiring indicates business growth." in intel.strengths
    assert "Layoff announcements increase operational uncertainty." in intel.weaknesses
    assert "High growth opportunity." in intel.opportunities
    assert "Attractive investment profile." in intel.opportunities
    assert (
        "TestCompany generated 5 strategic business events." in intel.executive_summary
    )
