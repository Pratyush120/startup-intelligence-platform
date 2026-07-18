"""
Persistence Repository

Handles all database read/write operations for the SDIP pipeline.
"""

import json
from datetime import datetime, timezone
from typing import Set, List, Optional

from src.database.db import Database
from src.utils.logger import get_logger
import time

logger = get_logger(__name__)


class SimpleCache:
    """Lightweight in-memory TTL cache."""

    def __init__(self, ttl_seconds: int = 60):
        self.ttl = ttl_seconds
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            val, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return val
            del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())


# Global cache instance for the repository
repo_cache = SimpleCache(ttl_seconds=60)


class Repository:
    def __init__(self):
        self.db = Database()

    # ==========================================================
    # DEDUPLICATION
    # ==========================================================

    def get_all_url_hashes(self) -> Set[str]:
        """Returns all url_hash values from the articles table."""
        self.db.execute("SELECT url_hash FROM articles WHERE url_hash IS NOT NULL")
        rows = self.db.fetchall()
        return {row["url_hash"] for row in rows}

    # ==========================================================
    # ARTICLES
    # ==========================================================

    def save_article(self, record) -> Optional[int]:
        """Saves a raw article record. Returns article_id or None if duplicate."""
        url_hash = record.metadata.get("url_hash", "")
        try:
            self.db.execute(
                """
                INSERT OR IGNORE INTO articles(
                    url_hash, title, description, url, publisher,
                    article_type, published_at, collected_at, processed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    url_hash,
                    record.title,
                    record.description,
                    record.url,
                    record.metadata.get("publisher", "Unknown"),
                    record.metadata.get("article_type", ""),
                    record.published_at,
                    record.collected_at,
                ),
            )
            self.db.execute(
                "SELECT article_id FROM articles WHERE url_hash = ?", (url_hash,)
            )
            row = self.db.fetchone()
            return row["article_id"] if row else None
        except Exception as e:
            logger.warning(f"Failed to save article: {e}")
            return None

    # ==========================================================
    # EVENTS
    # ==========================================================

    def save_event(self, event, article_id: Optional[int] = None):
        """Saves an enriched business event."""
        self.db.execute(
            """
            INSERT INTO events(
                article_id, company_name, event_type, article_type,
                title, ai_summary, business_impact, source,
                published_at, confidence, impact_score, importance_score,
                amount, currency, funding_round, risk_tags, opportunity_tags
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                article_id,
                getattr(event, "company", None) or "Unknown",
                getattr(event, "event_type", None) or "General",
                getattr(event, "article_type", None) or "",
                getattr(event, "title", None) or "",
                getattr(event, "ai_summary", None) or "",
                getattr(event, "business_impact", None) or "",
                getattr(event, "source", ""),
                getattr(event, "published_at", ""),
                getattr(event, "confidence", 0.5),
                getattr(event, "impact_score", 0.0),
                getattr(event, "importance_score", 0.0),
                getattr(event, "entities", {}).get("amount"),
                getattr(event, "entities", {}).get("currency"),
                getattr(event, "entities", {}).get("round"),
                getattr(event, "risk_tags", "[]"),
                getattr(event, "opportunity_tags", "[]"),
            ),
        )

    # ==========================================================
    # COMPANIES
    # ==========================================================

    def save_company(self, company):
        """Saves or updates a company profile."""
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute(
            """
            INSERT OR REPLACE INTO companies(
                company_name, momentum_score, growth_score, risk_score,
                investment_score, influence_score, business_health,
                total_funding, funding_events, hiring_events,
                layoff_events, expansion_events, acquisition_events,
                recommendation, confidence_grade, last_updated
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                getattr(company, "company_name", ""),
                getattr(company, "momentum_score", 0),
                getattr(company, "growth_score", 0),
                getattr(company, "risk_score", 0),
                getattr(company, "investment_score", 0),
                getattr(company, "influence_score", 0),
                getattr(company, "business_health", 0),
                getattr(company, "total_funding", 0),
                getattr(company, "funding_events", 0),
                getattr(company, "hiring_events", 0),
                getattr(company, "layoff_events", 0),
                getattr(company, "expansion_events", 0),
                getattr(company, "acquisition_events", 0),
                getattr(company, "recommendation", "Monitor"),
                getattr(company, "confidence_grade", "C"),
                now,
            ),
        )

    # ==========================================================
    # PIPELINE RUNS
    # ==========================================================

    def start_pipeline_run(self) -> int:
        """Records the start of a pipeline run. Returns run_id."""
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute("INSERT INTO pipeline_runs(started_at) VALUES (?)", (now,))
        self.db.execute("SELECT last_insert_rowid()")
        row = self.db.fetchone()
        return row[0] if row else 0

    def complete_pipeline_run(
        self,
        run_id: int,
        status: str,
        records_collected: int,
        records_processed: int,
        events_created: int,
        companies_updated: int,
        errors: int,
        duration_seconds: float,
        error_details: str = "",
    ):
        """Records the completion of a pipeline run."""
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute(
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
                error_details = ?
            WHERE run_id = ?
            """,
            (
                now,
                status,
                records_collected,
                records_processed,
                events_created,
                companies_updated,
                errors,
                round(duration_seconds, 2),
                error_details,
                run_id,
            ),
        )

    # ==========================================================
    # MARKET SNAPSHOTS
    # ==========================================================

    def save_market_snapshot(self, date: str, data: dict):
        """Upserts a daily market snapshot."""
        self.db.execute(
            """
            INSERT OR REPLACE INTO market_snapshots(
                date, funding_amount, hiring_events, layoff_events,
                expansion_events, acquisition_events, total_events,
                market_health
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                date,
                data.get("funding_amount", 0),
                data.get("hiring_events", 0),
                data.get("layoff_events", 0),
                data.get("expansion_events", 0),
                data.get("acquisition_events", 0),
                data.get("total_events", 0),
                data.get("market_health", 0),
            ),
        )

    # ==========================================================
    # COMPANY HISTORY
    # ==========================================================

    def save_company_history(
        self, company_name: str, date: str, momentum: float, event_count: int
    ):
        """Upserts a daily company history snapshot for sparklines."""
        self.db.execute(
            """
            INSERT OR REPLACE INTO company_history(
                company_name, date, momentum_score, event_count
            ) VALUES (?,?,?,?)
            """,
            (company_name, date, momentum, event_count),
        )

    def get_company_history(self, company_name: str, limit: int = 30) -> List[float]:
        """Returns the last N momentum scores for sparkline generation."""
        cache_key = f"company_history_{company_name}_{limit}"
        cached = repo_cache.get(cache_key)
        if cached is not None:
            return cached

        self.db.execute(
            """
            SELECT momentum_score FROM company_history
            WHERE company_name = ?
            ORDER BY date ASC
            LIMIT ?
            """,
            (company_name, limit),
        )
        rows = self.db.fetchall()
        result = [float(row["momentum_score"]) for row in rows]
        repo_cache.set(cache_key, result)
        return result

    # ==========================================================
    # EXECUTIVE BRIEFS
    # ==========================================================

    def save_executive_brief(self, brief: dict):
        """Saves an executive brief into the database."""
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute(
            """
            INSERT INTO executive_briefs(
                generated_at, market_health_score, investment_climate,
                risk_level, growth_outlook, strategic_summary,
                confidence_score, primary_recommendation
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                now,
                brief.get("market_health_score", 0.0),
                brief.get("investment_climate", ""),
                brief.get("risk_level", ""),
                brief.get("growth_outlook", ""),
                brief.get("strategic_summary", ""),
                brief.get("confidence_score", 0.0),
                brief.get("primary_recommendation", ""),
            ),
        )

    def get_latest_executive_brief(self) -> Optional[dict]:
        """Returns the latest executive brief."""
        self.db.execute(
            """
            SELECT * FROM executive_briefs
            ORDER BY generated_at DESC LIMIT 1
            """
        )
        row = self.db.fetchone()
        return dict(row) if row else None

    # ==========================================================
    # RECOMMENDATIONS
    # ==========================================================

    def save_recommendations(self, recommendations: List[dict]):
        """Saves strategic recommendations."""
        now = datetime.now(timezone.utc).isoformat()
        for rec in recommendations:
            self.db.execute(
                """
                INSERT INTO recommendations(
                    title, reason, priority, confidence, evidence_score,
                    strategic_impact, opportunity_est, risk_est,
                    suggested_action, related_companies, related_event_ids,
                    generated_at, is_active
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,1)
                """,
                (
                    rec.get("title", ""),
                    rec.get("reason", ""),
                    rec.get("priority", "Medium"),
                    rec.get("confidence", 0.0),
                    rec.get("evidence_score", 0.0),
                    rec.get("strategic_impact", ""),
                    rec.get("opportunity_est", ""),
                    rec.get("risk_est", ""),
                    rec.get("suggested_action", ""),
                    json.dumps(rec.get("related_companies", [])),
                    json.dumps(rec.get("related_event_ids", [])),
                    now,
                ),
            )

    def get_recommendations(self, limit: int = 10, offset: int = 0) -> List[dict]:
        """Returns active recommendations."""
        self.db.execute(
            """
            SELECT * FROM recommendations
            WHERE is_active = 1
            ORDER BY priority DESC, confidence DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return [dict(row) for row in self.db.fetchall()]

    # ==========================================================
    # READ: COMPANIES (WITH PAGINATION & FILTERING)
    # ==========================================================

    def get_top_companies(
        self, limit: int = 25, offset: int = 0, sector: str = None
    ) -> List[dict]:
        """Returns top companies ordered by momentum score."""
        cache_key = f"companies_{limit}_{offset}_{sector}"
        cached = repo_cache.get(cache_key)
        if cached is not None:
            return cached

        query = "SELECT * FROM companies"
        params = []
        if sector:
            query += " WHERE sector = ?"
            params.append(sector)
        query += " ORDER BY momentum_score DESC, growth_score DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        self.db.execute(query, tuple(params))
        result = [dict(row) for row in self.db.fetchall()]
        repo_cache.set(cache_key, result)
        return result

    def get_company_by_id(self, company_id: int) -> Optional[dict]:
        self.db.execute("SELECT * FROM companies WHERE company_id = ?", (company_id,))
        row = self.db.fetchone()
        return dict(row) if row else None

    # ==========================================================
    # READ: EVENTS (TIMELINE)
    # ==========================================================

    def get_recent_events(
        self, limit: int = 50, offset: int = 0, event_type: str = None
    ) -> List[dict]:
        """Returns recent events for timeline."""
        query = "SELECT * FROM events"
        params = []
        if event_type:
            query += " WHERE event_type = ?"
            params.append(event_type)
        query += " ORDER BY published_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        self.db.execute(query, tuple(params))
        return [dict(row) for row in self.db.fetchall()]

    # ==========================================================
    # READ: MARKET SNAPSHOTS
    # ==========================================================

    def get_latest_market_snapshot(self) -> Optional[dict]:
        self.db.execute("SELECT * FROM market_snapshots ORDER BY date DESC LIMIT 1")
        row = self.db.fetchone()
        return dict(row) if row else None

    # ==========================================================
    # PIPELINE RUN STATUS
    # ==========================================================

    def get_latest_pipeline_run(self) -> Optional[dict]:
        self.db.execute("SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 1")
        row = self.db.fetchone()
        return dict(row) if row else None

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search_entities(
        self, query: str, limit: int = 20, offset: int = 0
    ) -> List[dict]:
        search_term = f"%{query}%"
        self.db.execute(
            """
            SELECT * FROM companies
            WHERE company_name LIKE ? OR sector LIKE ?
            ORDER BY momentum_score DESC
            LIMIT ? OFFSET ?
            """,
            (search_term, search_term, limit, offset),
        )
        return [dict(row) for row in self.db.fetchall()]

    def search_events(self, query: str, limit: int = 20, offset: int = 0) -> List[dict]:
        search_term = f"%{query}%"
        self.db.execute(
            """
            SELECT * FROM events
            WHERE company_name LIKE ? OR title LIKE ? OR event_type LIKE ?
            ORDER BY published_at DESC
            LIMIT ? OFFSET ?
            """,
            (search_term, search_term, search_term, limit, offset),
        )
        return [dict(row) for row in self.db.fetchall()]

    # ==========================================================
    # CLOSE
    # ==========================================================

    def close(self):
        self.db.close()
