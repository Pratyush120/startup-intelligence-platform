import os
from unittest.mock import patch
from src.pipeline.llm_analyzer import LLMAnalyzer
from src.services.providers.gemini_provider import GeminiProvider
from src.models.intelligence import EventAnalysisResponse

os.environ["GEMINI_API_KEY"] = "test_key"


def test_gemini_provider_mock():
    # Test that GeminiProvider handles mocked responses properly
    provider = GeminiProvider()

    with patch.object(provider, "analyze_event") as mock_analyze:
        mock_analyze.return_value = EventAnalysisResponse(
            executive_summary="Gemini Summary",
            business_impact="High Impact",
            risk="Low Risk",
            opportunity="Huge Opportunity",
            key_insight="Strategic move",
            confidence=0.85,
            token_usage=150,
            processing_time_ms=500,
        )

        # Test direct call to provider
        res = provider.analyze_event(
            title="Test", description="Desc", event_type="Funding", company="Startup"
        )
        assert isinstance(res, EventAnalysisResponse)
        assert res.executive_summary == "Gemini Summary"
        assert res.confidence == 0.85
        assert res.token_usage == 150


def test_llm_analyzer_with_gemini():
    analyzer = LLMAnalyzer()
    assert analyzer.provider is not None
    assert isinstance(analyzer.provider, GeminiProvider)

    # Mock the underlying provider's analyze_event method
    with patch.object(analyzer.provider, "analyze_event") as mock_analyze:
        mock_analyze.return_value = EventAnalysisResponse(
            executive_summary="Sum",
            business_impact="Impact",
            risk="Risk",
            opportunity="Opp",
            key_insight="Insight",
            confidence=0.9,
            token_usage=10,
            processing_time_ms=100,
        )

        # Call the analyzer
        res = analyzer.analyze("T", "D", "E", "C")
        assert res.executive_summary == "Sum"
        assert res.key_insight == "Insight"
        assert res.confidence == 0.9
