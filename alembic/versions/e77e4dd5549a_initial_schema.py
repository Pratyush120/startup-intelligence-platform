"""Initial schema

Revision ID: e77e4dd5549a
Revises:
Create Date: 2026-07-19 12:42:06.842665

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e77e4dd5549a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use IF NOT EXISTS for safe initial application on existing databases
    op.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            article_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            url_hash      TEXT UNIQUE,
            title         TEXT NOT NULL,
            description   TEXT,
            url           TEXT,
            publisher     TEXT,
            language      TEXT DEFAULT 'en',
            article_type  TEXT,
            published_at  TEXT,
            collected_at  TEXT NOT NULL,
            processed     INTEGER DEFAULT 0
        )
    """)
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_articles_processed ON articles(processed)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_at)"
    )

    op.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name     TEXT UNIQUE NOT NULL,
            sector           TEXT,
            momentum_score   REAL DEFAULT 0,
            growth_score     REAL DEFAULT 0,
            risk_score       REAL DEFAULT 0,
            investment_score REAL DEFAULT 0,
            influence_score  REAL DEFAULT 0,
            business_health  REAL DEFAULT 0,
            total_funding    REAL DEFAULT 0,
            funding_events   INTEGER DEFAULT 0,
            hiring_events    INTEGER DEFAULT 0,
            layoff_events    INTEGER DEFAULT 0,
            expansion_events INTEGER DEFAULT 0,
            acquisition_events INTEGER DEFAULT 0,
            recommendation   TEXT,
            confidence_grade TEXT,
            last_updated     TEXT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id       INTEGER REFERENCES articles(article_id),
            company_name     TEXT NOT NULL,
            event_type       TEXT NOT NULL,
            article_type     TEXT,
            title            TEXT,
            ai_summary       TEXT,
            business_impact  TEXT,
            source           TEXT,
            published_at     TEXT,
            confidence       REAL,
            impact_score     REAL,
            importance_score REAL,
            amount           REAL,
            currency         TEXT,
            funding_round    TEXT,
            risk_tags        TEXT,
            opportunity_tags TEXT
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_events_company ON events(company_name)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_events_published ON events(published_at)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_events_company_date ON events(company_name, published_at DESC)"
    )

    op.execute("""
        CREATE TABLE IF NOT EXISTS company_history (
            history_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name   TEXT NOT NULL,
            date           TEXT NOT NULL,
            momentum_score REAL,
            event_count    INTEGER,
            UNIQUE(company_name, date)
        )
    """)
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_history_company_date ON company_history(company_name, date)"
    )

    op.execute("""
        CREATE TABLE IF NOT EXISTS market_snapshots (
            snapshot_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            date               TEXT UNIQUE NOT NULL,
            funding_amount     REAL DEFAULT 0,
            hiring_events      INTEGER DEFAULT 0,
            layoff_events      INTEGER DEFAULT 0,
            expansion_events   INTEGER DEFAULT 0,
            acquisition_events INTEGER DEFAULT 0,
            total_events       INTEGER DEFAULT 0,
            market_health      REAL
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS strategic_alerts (
            alert_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title          TEXT NOT NULL,
            company_name   TEXT,
            category       TEXT,
            priority       TEXT,
            impact         TEXT,
            recommendation TEXT,
            confidence     REAL,
            timestamp      TEXT NOT NULL,
            is_active      INTEGER DEFAULT 1,
            evidence_ids   TEXT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS executive_briefs (
            brief_id               INTEGER PRIMARY KEY AUTOINCREMENT,
            generated_at           TEXT NOT NULL,
            market_health_score    REAL,
            investment_climate     TEXT,
            risk_level             TEXT,
            growth_outlook         TEXT,
            strategic_summary      TEXT,
            confidence_score       REAL,
            primary_recommendation TEXT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            rec_id            INTEGER PRIMARY KEY AUTOINCREMENT,
            title             TEXT NOT NULL,
            reason            TEXT,
            priority          TEXT,
            confidence        REAL,
            evidence_score    REAL,
            strategic_impact  TEXT,
            opportunity_est   TEXT,
            risk_est          TEXT,
            suggested_action  TEXT,
            related_companies TEXT,
            related_event_ids TEXT,
            generated_at      TEXT NOT NULL,
            is_active         INTEGER DEFAULT 1
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            run_id            INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at        TEXT NOT NULL,
            completed_at      TEXT,
            status            TEXT DEFAULT 'running',
            records_collected  INTEGER DEFAULT 0,
            records_processed  INTEGER DEFAULT 0,
            events_created     INTEGER DEFAULT 0,
            companies_updated  INTEGER DEFAULT 0,
            errors             INTEGER DEFAULT 0,
            duration_seconds   REAL,
            error_details      TEXT,
            llm_provider       TEXT,
            total_tokens       INTEGER DEFAULT 0,
            total_llm_time_ms  INTEGER DEFAULT 0
        )
    """)


def downgrade() -> None:
    # We do not drop tables on downgrade to prevent data loss in this environment
    pass
