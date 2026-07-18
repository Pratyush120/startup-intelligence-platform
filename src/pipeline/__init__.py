"""
Pipeline Module — Public API
"""

from src.pipeline.preprocessor import Preprocessor
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.importance_scorer import ImportanceScorer
from src.pipeline.llm_analyzer import LLMAnalyzer, LLMAnalysis
from src.pipeline.sparkline_generator import SparklineGenerator
from src.pipeline.api_serializer import (
    serialize_executive_brief,
    serialize_metric_cards,
    serialize_company_metrics,
    serialize_market_snapshots,
    serialize_strategic_alerts,
    serialize_timeline_events,
    serialize_recommendations,
)
from src.pipeline.orchestrator import PipelineOrchestrator, PipelineResult

__all__ = [
    "Preprocessor",
    "Deduplicator",
    "ImportanceScorer",
    "LLMAnalyzer",
    "LLMAnalysis",
    "SparklineGenerator",
    "serialize_executive_brief",
    "serialize_metric_cards",
    "serialize_company_metrics",
    "serialize_market_snapshots",
    "serialize_strategic_alerts",
    "serialize_timeline_events",
    "serialize_recommendations",
    "PipelineOrchestrator",
    "PipelineResult",
]
