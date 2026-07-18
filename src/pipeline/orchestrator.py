"""
Pipeline Orchestrator

Single entry point for the SDIP intelligence pipeline.
Each step handles its own errors without aborting the entire run.
Records pipeline run metrics to the pipeline_runs audit table.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, List

from src.collectors.newsapi_collector import NewsAPICollector
from src.collectors.google_news_collector import GoogleNewsCollector
from src.collectors.mock_collector import MockCollector

from src.pipeline.preprocessor import Preprocessor
from src.pipeline.deduplicator import Deduplicator
from src.pipeline.classifier import Classifier
from src.pipeline.importance_scorer import ImportanceScorer
from src.pipeline.llm_analyzer import LLMAnalyzer
from src.pipeline.sparkline_generator import SparklineGenerator
from src.pipeline.api_serializer import (
    serialize_executive_brief,
    serialize_metric_cards,
    serialize_company_metrics,
    serialize_market_snapshots,
    serialize_timeline_events,
)

from src.intelligence.intelligence_engine import IntelligenceEngine
from src.analytics.company_store import CompanyStore
from src.analytics.market_engine import MarketEngine
from src.analytics.executive_engine import ExecutiveEngine
from src.analytics.trend_engine import TrendEngine

from src.database.schema import SchemaManager
from src.database.repository import Repository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PipelineResult:
    """Holds the fully serialized output of one pipeline run."""

    def __init__(self):
        self.executive_brief: dict[str, Any] = {}
        self.metric_cards: list[dict] = []
        self.market_snapshots: list[dict] = []
        self.strategic_alerts: list[dict] = []
        self.timeline_events: list[dict] = []
        self.top_companies: list[dict] = []
        self.recommendations: list[dict] = []
        self.run_metadata: dict[str, Any] = {}


class PipelineOrchestrator:
    """
    Orchestrates the full SDIP intelligence pipeline.
    Each step handles its own errors without aborting the entire run.
    """

    def run(self) -> PipelineResult:
        result = PipelineResult()
        start_time = datetime.now(timezone.utc)
        error_count = 0
        error_details: List[str] = []

        # LLM Metrics Tracking
        total_tokens = 0
        total_llm_time_ms = 0
        llm_provider_name = "MockProvider"

        logger.info("=" * 60)
        logger.info("SDIP Intelligence Pipeline — START")
        logger.info("=" * 60)

        # ------------------------------------------------------------------
        # STEP 0: Schema + Audit trail
        # ------------------------------------------------------------------
        try:
            SchemaManager().create_tables()
            logger.info("Step 0: Schema ready.")
        except Exception as e:
            logger.error(f"Step 0 FAILED: {e}")
            result.run_metadata = {"status": "schema_error", "error": str(e)}
            return result

        repository = Repository()
        run_id = repository.start_pipeline_run()

        # ------------------------------------------------------------------
        # STEP 1: Collect (Fallback logic)
        # ------------------------------------------------------------------
        raw_records = []
        try:
            # 1. Try NewsAPI if key exists
            collector = NewsAPICollector()
            raw_records = collector.collect()

            # 2. Try Google News (RSS) if NewsAPI returned empty
            if not raw_records:
                logger.info("NewsAPI returned empty, trying Google News RSS...")
                collector = GoogleNewsCollector()
                raw_records = collector.collect()

            # 3. Fallback to Mock Collector
            if not raw_records:
                logger.info("RSS returned empty, falling back to MockCollector...")
                collector = MockCollector()
                raw_records = collector.collect()

            logger.info(
                f"Step 1: Collected {len(raw_records)} raw records via {collector.__class__.__name__}."
            )
        except Exception as e:
            logger.error(f"Step 1 FAILED: {e}")
            error_count += 1
            error_details.append(f"Collector: {e}")

        if not raw_records:
            logger.warning("No records collected. Recording empty run.")
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            repository.complete_pipeline_run(
                run_id=run_id,
                status="no_data",
                records_collected=0,
                records_processed=0,
                events_created=0,
                companies_updated=0,
                errors=error_count,
                duration_seconds=duration,
                error_details="; ".join(error_details),
            )
            repository.close()
            result.run_metadata = {"status": "no_data"}
            return result

        # ------------------------------------------------------------------
        # STEP 2: Preprocess
        # ------------------------------------------------------------------
        try:
            preprocessor = Preprocessor()
            clean_records = preprocessor.process(raw_records)
            logger.info(f"Step 2: {len(clean_records)} records after preprocessing.")
        except Exception as e:
            logger.error(f"Step 2 FAILED: {e}")
            error_count += 1
            error_details.append(f"Preprocessor: {e}")
            clean_records = raw_records

        # ------------------------------------------------------------------
        # STEP 3: Deduplicate (seeded from DB)
        # ------------------------------------------------------------------
        try:
            existing_hashes = repository.get_all_url_hashes()
            deduplicator = Deduplicator(existing_hashes=existing_hashes)
            unique_records = deduplicator.deduplicate(clean_records)
            logger.info(f"Step 3: {len(unique_records)} unique records.")
        except Exception as e:
            logger.error(f"Step 3 FAILED: {e}")
            error_count += 1
            error_details.append(f"Deduplicator: {e}")
            unique_records = clean_records

        # ------------------------------------------------------------------
        # STEP 3b: Classify Engine (18 categories)
        # ------------------------------------------------------------------
        try:
            classifier = Classifier()
            classified_records = classifier.classify(unique_records)
            logger.info(f"Step 3b: Classified {len(classified_records)} records.")
        except Exception as e:
            logger.error(f"Step 3b FAILED: {e}")
            error_count += 1
            error_details.append(f"Classifier: {e}")
            classified_records = unique_records

        # ------------------------------------------------------------------
        # STEP 3c: Save articles to DB
        # ------------------------------------------------------------------
        article_ids = {}
        for record in classified_records:
            try:
                aid = repository.save_article(record)
                if aid:
                    article_ids[record.title] = aid
            except Exception as e:
                logger.warning(f"Article save failed: {e}")

        # ------------------------------------------------------------------
        # STEP 4: Extract Events (Entity Recognition via Engine)
        # ------------------------------------------------------------------
        events = []
        try:
            engine = IntelligenceEngine()
            events = engine.process_many(classified_records)
            logger.info(f"Step 4: {len(events)} business events extracted.")
        except Exception as e:
            logger.error(f"Step 4 FAILED: {e}")
            error_count += 1
            error_details.append(f"IntelligenceEngine: {e}")

        # ------------------------------------------------------------------
        # STEP 5: Importance scoring + LLM analysis
        # ------------------------------------------------------------------
        importance_scorer = ImportanceScorer()

        # Initialize LLM with Provider Abstraction (Mock-first architecture constraint)
        llm_analyzer = LLMAnalyzer()
        llm_provider_name = llm_analyzer.provider.__class__.__name__

        enriched_events = []

        for event in events:
            try:
                # Need to cast event attributes into a Record for the ImportanceScorer
                from src.models.record import Record

                temp_rec = Record(
                    source=getattr(event, "source", ""),
                    title=getattr(event, "title", ""),
                    description=getattr(event, "title", ""),
                    url="",
                    published_at=getattr(event, "published_at", None),
                    collected_at="",
                    record_type="news",
                    metadata={
                        "publisher": getattr(event, "source", ""),
                        "category": getattr(event, "event_type", "General"),
                        "confidence": float(getattr(event, "confidence", 0.5)),
                    },
                )

                importance = importance_scorer.score(temp_rec)

                analysis = llm_analyzer.analyze(
                    title=getattr(event, "title", None) or "",
                    description=getattr(event, "title", None) or "",
                    event_type=getattr(event, "event_type", None) or "General",
                    company=getattr(event, "company", None) or "Unknown",
                )

                total_tokens += analysis.token_usage
                total_llm_time_ms += analysis.processing_time_ms

                event.importance_score = importance
                event.ai_summary = analysis.executive_summary
                event.business_impact = analysis.business_impact
                # Risk and opportunity tags from LLM mapped to JSON array strings
                event.risk_tags = json.dumps([analysis.risk])
                event.opportunity_tags = json.dumps([analysis.opportunity])

                original_conf = float(getattr(event, "confidence", 0.7))
                event.confidence = round((original_conf + analysis.confidence) / 2, 3)

                enriched_events.append(event)
            except Exception as e:
                logger.warning(f"Event enrichment failed: {e}")
                error_count += 1
                enriched_events.append(event)

        logger.info(f"Step 5: {len(enriched_events)} events enriched.")

        # ------------------------------------------------------------------
        # STEP 6: Company aggregation
        # ------------------------------------------------------------------
        company_intelligences = []
        try:
            company_store = CompanyStore()
            company_store.process(enriched_events)
            companies_list = company_store.top_companies(limit=500)

            from src.analytics.feature_engineering import FeatureEngineeringEngine
            from src.analytics.scoring_engine import ScoringEngine
            from src.analytics.company_engine import CompanyEngine

            features_dict = FeatureEngineeringEngine().build(enriched_events)
            scoring_engine = ScoringEngine()
            company_engine = CompanyEngine()

            for c in companies_list:
                features = features_dict.get(c.company_name)
                if features:
                    scores = scoring_engine.score(features)
                    intel = company_engine.build(features, scores)
                    company_intelligences.append(intel)

            logger.info(f"Step 6: {len(company_intelligences)} companies aggregated.")
        except Exception as e:
            logger.error(f"Step 6 FAILED: {e}")
            error_count += 1
            error_details.append(f"CompanyEngine: {e}")

        # ------------------------------------------------------------------
        # STEP 7: Market intelligence
        # ------------------------------------------------------------------
        market = None
        try:
            market_engine = MarketEngine()
            market = market_engine.build(company_intelligences)
            logger.info(
                f"Step 7: Market built — health={getattr(market, 'market_health', 'N/A')}"
            )
        except Exception as e:
            logger.error(f"Step 7 FAILED: {e}")
            error_count += 1
            error_details.append(f"MarketEngine: {e}")

        # ------------------------------------------------------------------
        # STEP 8: Executive brief & Recommendations
        # ------------------------------------------------------------------
        brief_model = None
        raw_recommendations = []
        try:
            trend_engine = TrendEngine()
            trend = trend_engine.analyse(market)
            executive_engine = ExecutiveEngine()
            brief_model = executive_engine.generate(market, trend)
            logger.info("Step 8a: Executive brief generated.")

            from src.analytics.recommendation_engine import RecommendationEngine

            rec_engine = RecommendationEngine()
            for ci in company_intelligences[
                :10
            ]:  # Top 10 companies get recommendations
                rec = rec_engine.recommend(ci)
                # Map CompanyRecommendation to the dict format expected by repository
                raw_recommendations.append(
                    {
                        "title": f"{rec.recommendation} - {rec.company_name}",
                        "reason": " ".join(rec.rationale),
                        "priority": "High" if rec.priority <= 2 else "Medium",
                        "confidence": 0.9 if rec.confidence == "Very High" else 0.7,
                        "suggested_action": " ".join(rec.actions),
                        "related_companies": [rec.company_name],
                    }
                )
            logger.info("Step 8b: Recommendations generated.")
        except Exception as e:
            logger.error(f"Step 8 FAILED: {e}")
            error_count += 1
            error_details.append(f"ExecutiveEngine/Recommendations: {e}")

        # ------------------------------------------------------------------
        # STEP 9: Persist
        # ------------------------------------------------------------------
        try:
            for event in enriched_events:
                aid = article_ids.get(getattr(event, "title", ""))
                repository.save_event(event, article_id=aid)

            for company in companies_list:
                repository.save_company(company)

            # Save daily company history for sparklines
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            for ci in company_intelligences:
                repository.save_company_history(
                    ci.company_name,
                    today,
                    getattr(ci, "business_health", 0),
                    getattr(ci, "total_events", 0),
                )

            # Save market snapshot
            if market:
                repository.save_market_snapshot(
                    today,
                    {
                        "funding_amount": getattr(market, "total_funding", 0),
                        "hiring_events": getattr(market, "hiring_events", 0),
                        "layoff_events": getattr(market, "layoff_events", 0),
                        "expansion_events": getattr(market, "expansion_events", 0),
                        "acquisition_events": getattr(market, "acquisition_events", 0),
                        "total_events": getattr(market, "total_events", 0),
                        "market_health": getattr(market, "market_health", 0),
                    },
                )

            # Persist Recommendations
            if raw_recommendations:
                repository.save_recommendations(raw_recommendations)

            # Serialize & Persist Executive Brief
            if brief_model and market:
                result.executive_brief = serialize_executive_brief(
                    brief_id="latest",
                    market_health_score=getattr(market, "market_health", 50),
                    investment_climate=_map_investment_climate(
                        getattr(market, "investment_climate", "Moderate")
                    ),
                    risk_level=_map_risk_climate(
                        getattr(market, "risk_climate", "Moderate")
                    ),
                    growth_outlook=_map_growth_climate(
                        getattr(market, "growth_climate", "Stable")
                    ),
                    strategic_summary=brief_model.overview,
                    confidence_score=getattr(market, "average_confidence", 0.75),
                    primary_recommendation=(
                        brief_model.strategic_actions[0]
                        if brief_model.strategic_actions
                        else "Monitor market developments closely."
                    ),
                )
                repository.save_executive_brief(result.executive_brief)

            logger.info(
                "Step 9: Persisted events, companies, history, snapshots, recs, and brief."
            )
        except Exception as e:
            logger.error(f"Step 9 FAILED: {e}")
            error_count += 1
            error_details.append(f"Persistence: {e}")

        # ------------------------------------------------------------------
        # STEP 10: Generate API-ready output
        # ------------------------------------------------------------------
        try:
            sparkline_gen = SparklineGenerator()
            sparklines = {}
            for ci in company_intelligences:
                history = repository.get_company_history(ci.company_name)
                sparklines[ci.company_name] = sparkline_gen.generate(
                    history if history else [getattr(ci, "business_health", 50)]
                )

            result.top_companies = serialize_company_metrics(
                company_intelligences[:25], sparklines
            )

            result.timeline_events = serialize_timeline_events(
                sorted(
                    enriched_events,
                    key=lambda e: str(getattr(e, "published_at", "")),
                    reverse=True,
                )[:50]
            )

            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            funding_today = getattr(market, "total_funding", 0) if market else 0
            hiring_today = getattr(market, "hiring_events", 0) if market else 0
            layoff_today = getattr(market, "layoff_events", 0) if market else 0

            result.market_snapshots = serialize_market_snapshots(
                [
                    {
                        "date": today,
                        "funding_amount": funding_today,
                        "hiring_events": hiring_today,
                        "layoff_events": layoff_today,
                    }
                ]
            )

            result.metric_cards = serialize_metric_cards(
                total_companies=len(company_intelligences),
                funding_today=funding_today,
                total_events=len(enriched_events),
                market_health=getattr(market, "market_health", 50) if market else 50,
                avg_confidence=getattr(market, "average_confidence", 0.7)
                if market
                else 0.7,
                companies_sparkline=[50.0] * 5,
                funding_sparkline=[50.0] * 5,
                events_sparkline=[50.0] * 5,
                health_sparkline=[50.0] * 5,
            )

            logger.info("Step 10: API output serialized.")
        except Exception as e:
            logger.error(f"Step 10 FAILED: {e}")
            error_count += 1
            error_details.append(f"Serialization: {e}")

        # ------------------------------------------------------------------
        # Record pipeline run metrics
        # ------------------------------------------------------------------
        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()

        status = "success" if error_count == 0 else "completed_with_errors"

        # Note: repository.complete_pipeline_run will need to be updated to accept the new arguments!
        try:
            # We will use direct sql query to update the DB since repository.py signature might not take these yet,
            # wait, I'll update repository.py as well.
            repository.db.execute(
                """
                UPDATE pipeline_runs SET
                    completed_at = ?,
                    status = ?,
                    records_collected = ?,
                    records_processed = ?,
                    events_created = ?,
                    companies_updated = ?,
                    errors = ?,
                    duration_seconds = ?,
                    error_details = ?,
                    llm_provider = ?,
                    total_tokens = ?,
                    total_llm_time_ms = ?
                WHERE run_id = ?
                """,
                (
                    end_time.isoformat(),
                    status,
                    len(raw_records),
                    len(enriched_events),
                    len(enriched_events),
                    len(company_intelligences),
                    error_count,
                    round(duration, 2),
                    "; ".join(error_details),
                    llm_provider_name,
                    total_tokens,
                    total_llm_time_ms,
                    run_id,
                ),
            )
        except Exception as e:
            logger.warning(f"Failed to save advanced metrics to pipeline_runs: {e}")
            repository.complete_pipeline_run(
                run_id=run_id,
                status=status,
                records_collected=len(raw_records),
                records_processed=len(enriched_events),
                events_created=len(enriched_events),
                companies_updated=len(company_intelligences),
                errors=error_count,
                duration_seconds=duration,
                error_details="; ".join(error_details),
            )
        repository.close()

        result.run_metadata = {
            "run_id": run_id,
            "status": status,
            "started_at": start_time.isoformat(),
            "completed_at": end_time.isoformat(),
            "duration_seconds": round(duration, 2),
            "records_collected": len(raw_records),
            "records_processed": len(enriched_events),
            "companies_identified": len(company_intelligences),
            "errors": error_count,
        }

        logger.info(
            f"Pipeline complete in {duration:.1f}s — "
            f"{len(enriched_events)} events, "
            f"{len(company_intelligences)} companies, "
            f"{error_count} errors."
        )
        logger.info("=" * 60)

        return result


# ---------------------------------------------------------------------------
# Enum mappers (internal engine values → frontend TypeScript enum values)
# ---------------------------------------------------------------------------


def _map_investment_climate(raw: str) -> str:
    return {
        "Excellent": "Favorable",
        "Healthy": "Favorable",
        "Moderate": "Neutral",
        "Weak": "Neutral",
        "Poor": "Hostile",
    }.get(raw, "Neutral")


def _map_risk_climate(raw: str) -> str:
    return {
        "Critical": "Critical",
        "High": "High",
        "Moderate": "Medium",
        "Low": "Low",
    }.get(raw, "Medium")


def _map_growth_climate(raw: str) -> str:
    return {
        "Hyper Growth": "Accelerating",
        "High Growth": "Accelerating",
        "Growing": "Accelerating",
        "Stable": "Stable",
        "Slow": "Decelerating",
    }.get(raw, "Stable")
