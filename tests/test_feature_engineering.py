from src.analytics.feature_engineering import FeatureEngineeringEngine
from src.models.events.business_event import BusinessEvent


def test_feature_engineering_build():
    events = [
        BusinessEvent(
            company="TestCompany",
            event_type="Funding",
            title="Raised Series A",
            confidence=0.9,
            impact_score=0.8,
            source="TechCrunch",
            entities={"amount": "10000000"},
        ),
        BusinessEvent(
            company="TestCompany",
            event_type="Hiring",
            title="Hiring 100 engineers",
            confidence=0.8,
            impact_score=0.5,
            source="TechCrunch",
        ),
        BusinessEvent(
            company="TestCompany",
            event_type="Layoff",
            title="Layoffs announced",
            confidence=1.0,
            impact_score=0.9,
            source="WSJ",
        ),
        BusinessEvent(
            company="TestCompany",
            event_type="Expansion",
            title="Expansion to UK",
            confidence=0.7,
            impact_score=0.6,
            source="WSJ",
        ),
        BusinessEvent(
            company="TestCompany",
            event_type="Acquisition",
            title="Acquired by BigCorp",
            confidence=0.9,
            impact_score=0.9,
            source="Bloomberg",
        ),
        BusinessEvent(
            company=None,
            event_type="Funding",
            title="Unknown startup raises",
            confidence=0.5,
            impact_score=0.5,
            source="Unknown",
        ),
    ]

    engine = FeatureEngineeringEngine()
    features_dict = engine.build(events)

    assert "TestCompany" in features_dict
    features = features_dict["TestCompany"]

    assert features.total_events == 5
    assert features.funding_events == 1
    assert features.hiring_events == 1
    assert features.layoff_events == 1
    assert features.expansion_events == 1
    assert features.acquisition_events == 1
    assert features.total_funding == 10000000.0

    assert features.source_diversity == 3  # TechCrunch, WSJ, Bloomberg
    assert features.event_diversity == 5

    assert features.momentum > 0
