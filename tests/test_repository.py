import pytest
from src.database.repository import Repository
from src.analytics.company_engine import CompanyIntelligence

from src.database.schema import SchemaManager
from src.database.repository import repo_cache


@pytest.fixture
def repo():
    # Make sure tables exist
    SchemaManager().create_tables()
    repo_cache.cache.clear()
    return Repository()


def test_repo_save_company_and_get(repo):
    intel = CompanyIntelligence(
        company_name="RepoTestCompany",
        total_events=1,
        funding_events=1,
        hiring_events=0,
        layoff_events=0,
        expansion_events=0,
        acquisition_events=0,
        total_funding=100.0,
        average_confidence=0.9,
        average_impact=0.9,
        event_diversity=1,
        source_diversity=1,
        momentum=10.0,
        latest_event="Test",
        latest_event_type="Test",
        latest_event_date="2024",
        business_health=50.0,
        growth_score=50.0,
        investment_score=50.0,
        influence_score=50.0,
        risk_score=50.0,
        confidence_grade="A",
        recommendation="Buy",
        score_breakdown={},
        strengths=["Str"],
        weaknesses=["Weak"],
        opportunities=["Opp"],
        threats=["Threat"],
        executive_summary="Summary",
    )
    repo.save_company(intel)

    # Retrieve
    companies = repo.get_top_companies(limit=10)
    found = [c for c in companies if c["company_name"] == "RepoTestCompany"]
    assert len(found) > 0
    assert found[0]["business_health"] == 50.0


def test_repo_save_market_snapshot(repo):
    # create a mock brief
    brief = {
        "market_health_score": 80.0,
        "investment_climate": "Good",
        "risk_level": "Low",
        "growth_outlook": "Good",
        "strategic_summary": "Summary",
        "confidence_score": 0.8,
        "primary_recommendation": "Rec",
    }
    repo.save_executive_brief(brief)

    saved = repo.get_latest_executive_brief()
    assert saved is not None
