from unittest.mock import patch, MagicMock
from src.pipeline.llm_analyzer import (
    LLMAnalyzer,
    OpenAIProvider,
    MockProvider,
    LLMAnalysis,
)


def test_mock_provider():
    provider = MockProvider()
    analysis = provider.analyze("Test Title", "Test Desc", "Funding", "Startup")
    assert isinstance(analysis, LLMAnalysis)
    assert analysis.executive_summary != ""
    assert analysis.token_usage == 0


def test_openai_provider_fallback():
    import sys

    mock_openai = MagicMock()
    with patch.dict(sys.modules, {"openai": mock_openai}):
        # OpenAIProvider should fallback if no key or error
        provider = OpenAIProvider()

        mock_client = mock_openai.OpenAI.return_value
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        # When analyzing fails, OpenAI provider raises an exception, which the Analyzer catches.
        # So we should test Analyzer fallback.
        analyzer = LLMAnalyzer(provider=provider)
        analysis = analyzer.analyze("Test Title", "Test Desc", "Funding", "Startup")
        assert analysis.confidence == 0.75  # Mock provider fallback confidence


def test_llm_analyzer():
    analyzer = LLMAnalyzer()
    assert analyzer.provider is not None

    # Just mock the provider's analyze method
    with patch.object(analyzer.provider, "analyze") as mock_analyze:
        mock_analyze.return_value = LLMAnalysis(
            executive_summary="Sum",
            business_impact="Impact",
            risk="Risk",
            opportunity="Opp",
            confidence=0.9,
            token_usage=10,
            processing_time_ms=100,
        )

        res = analyzer.analyze("T", "D", "E", "C")
        assert res.executive_summary == "Sum"
