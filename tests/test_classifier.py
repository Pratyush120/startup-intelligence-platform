from src.models.record import Record
from src.pipeline.classifier import Classifier


def test_classifier_funding():
    record = Record(
        source="Mock",
        title="Startup raises $10M in Series A funding",
        description="",
        url="mock",
        published_at="2023",
        collected_at="2023",
        record_type="news",
        metadata={},
    )
    classifier = Classifier()
    results = classifier.classify([record])
    assert results[0].metadata["category"] == "Funding"
    assert results[0].metadata["confidence"] > 0.5


def test_classifier_layoffs():
    record = Record(
        source="Mock",
        title="Tech giant cuts 10% of jobs in major layoffs",
        description="",
        url="mock",
        published_at="2023",
        collected_at="2023",
        record_type="news",
        metadata={},
    )
    classifier = Classifier()
    results = classifier.classify([record])
    assert results[0].metadata["category"] == "Layoffs"
    assert results[0].metadata["confidence"] > 0.5


def test_classifier_fallback():
    record = Record(
        source="Mock",
        title="Some generic uninformative text",
        description="Nothing here",
        url="mock",
        published_at="2023",
        collected_at="2023",
        record_type="news",
        metadata={},
    )
    classifier = Classifier()
    results = classifier.classify([record])
    assert results[0].metadata["category"] == "Market Trend"
