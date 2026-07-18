import os
from unittest.mock import patch

# Force settings for testing
os.environ["ENVIRONMENT"] = "test"
os.environ["OPENAI_API_KEY"] = "mock_key"

from src.pipeline.orchestrator import PipelineOrchestrator


@patch("src.pipeline.orchestrator.Repository")
@patch("src.pipeline.orchestrator.SchemaManager")
def test_full_pipeline_run(MockSchema, MockRepo):
    # Setup mock repository
    mock_repo = MockRepo.return_value
    mock_repo.start_pipeline_run.return_value = 1
    mock_repo.get_all_url_hashes.return_value = set()
    mock_repo.get_company_history.return_value = [50.0, 52.0]

    # Fake News Records
    from src.models.record import Record
    import uuid

    random_hash = str(uuid.uuid4())
    fake_records = [
        Record(
            source="TechCrunch",
            title="AI Startup Anthropic raises $1B in Series D funding round",
            description="Anthropic announced a massive funding round.",
            url=f"http://test.com/{random_hash}",
            published_at="2024-01-01T00:00:00Z",
            collected_at="2024-01-01T00:00:00Z",
            record_type="news",
            metadata={"url_hash": random_hash},
        )
    ]

    with patch("src.pipeline.orchestrator.NewsAPICollector") as MockNews:
        mock_news = MockNews.return_value
        mock_news.collect.return_value = fake_records

        with patch("src.pipeline.orchestrator.GoogleNewsCollector") as MockGoogle:
            mock_google = MockGoogle.return_value
            mock_google.collect.return_value = []

            with patch("src.pipeline.orchestrator.LLMAnalyzer") as MockAnalyzer:
                mock_analyzer_instance = MockAnalyzer.return_value

                # Mock LLM Response for LLMAnalyzer
                class MockAnalysis:
                    def __init__(self):
                        self.executive_summary = "Test summary"
                        self.business_impact = "High impact"
                        self.risk = "Medium risk"
                        self.opportunity = "Growth"
                        self.confidence = 0.9
                        self.token_usage = 100
                        self.processing_time_ms = 500

                mock_analyzer_instance.analyze.return_value = MockAnalysis()

                # Execute Pipeline
                orchestrator = PipelineOrchestrator()
                result = orchestrator.run()

                # Verify that it ran correctly without mocking any internal engines!
                assert result is not None
                assert result.run_metadata["status"] == "success"
                assert result.run_metadata["records_processed"] >= 0
