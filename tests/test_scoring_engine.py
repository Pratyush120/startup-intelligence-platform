from src.analytics.scoring_engine import ScoringEngine
from src.analytics.feature_engineering import CompanyFeatures


def test_scoring_engine():
    features = CompanyFeatures(
        company_name="ScoreTestCompany",
        total_events=10,
        funding_events=2,
        hiring_events=5,
        layoff_events=1,
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
    )

    engine = ScoringEngine()
    score = engine.score(features)

    assert score.company_name == "ScoreTestCompany"
    assert score.business_health > 0
    assert score.growth_score > 0
    assert score.investment_score > 0
    assert score.influence_score > 0
    assert score.confidence_grade == "A+"
    assert score.recommendation != ""
    assert "Funding" in score.breakdown
    assert "Hiring" in score.breakdown
    assert "Expansion" in score.breakdown
    assert "Acquisition" in score.breakdown
    assert "Confidence" in score.breakdown
    assert "Impact" in score.breakdown
    assert "Momentum" in score.breakdown
    assert "Diversity" in score.breakdown
    assert "Layoff Penalty" in score.breakdown

    # Test low score
    bad_features = CompanyFeatures(
        company_name="BadCompany",
        layoff_events=5,
        average_confidence=0.5,
        event_diversity=1,
    )
    bad_score = engine.score(bad_features)

    assert bad_score.business_health == 0
    assert bad_score.confidence_grade == "D"
    assert bad_score.recommendation == "High Risk"
