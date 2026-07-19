"""
Database Seeder

Seeds the database with realistic initial data if it's completely empty.
Useful for ephemeral environments like Render where the database resets on deploy.
"""

from datetime import datetime, timezone, timedelta
from src.database.repository import Repository

from src.utils.logger import get_logger

logger = get_logger(__name__)


def seed_database_if_empty():
    repo = Repository()

    # Check if we already have companies
    repo.db.execute("SELECT COUNT(*) as count FROM companies")
    row = repo.db.fetchone()
    if row and row["count"] > 0:
        logger.info("Database already contains data. Skipping seed.")
        repo.close()
        return

    logger.info("Database is empty. Seeding initial data...")
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    # 1. Seed Market Snapshot
    repo.save_market_snapshot(
        today,
        {
            "funding_amount": 1250000000,
            "hiring_events": 45,
            "layoff_events": 12,
            "expansion_events": 8,
            "acquisition_events": 3,
            "total_events": 215,
            "market_health": 78.5,
        },
    )

    # 2. Seed Executive Brief
    repo.save_executive_brief(
        {
            "market_health_score": 78.5,
            "investment_climate": "Favorable",
            "risk_level": "Medium",
            "growth_outlook": "Accelerating",
            "strategic_summary": "The startup ecosystem is showing strong resilience with increased Series B funding rounds across AI and CleanTech sectors.",
            "confidence_score": 0.85,
            "primary_recommendation": "Increase allocation to AI infrastructure startups showing high momentum and low regulatory risk.",
        }
    )

    # 3. Seed Companies & History
    class DummyCompany:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    companies = [
        DummyCompany(
            company_name="Nexus Robotics",
            momentum_score=92.5,
            growth_score=88.0,
            risk_score=21.0,
            investment_score=95.0,
            influence_score=75.0,
            business_health=90.0,
            total_funding=45000000,
            recommendation="Strong Buy",
        ),
        DummyCompany(
            company_name="EcoStream AI",
            momentum_score=85.0,
            growth_score=91.0,
            risk_score=35.0,
            investment_score=82.0,
            influence_score=65.0,
            business_health=85.0,
            total_funding=12000000,
            recommendation="Buy",
        ),
        DummyCompany(
            company_name="DataFlow Systems",
            momentum_score=45.0,
            growth_score=30.0,
            risk_score=85.0,
            investment_score=20.0,
            influence_score=40.0,
            business_health=35.0,
            total_funding=85000000,
            recommendation="Sell",
        ),
    ]

    for c in companies:
        repo.save_company(c)
        # Seed 5 days of history for sparklines
        for i in range(5):
            d = (now - timedelta(days=4 - i)).strftime("%Y-%m-%d")
            base = c.momentum_score
            val = base - (4 - i) * 2 + (i % 2) * 3  # just some jitter
            repo.save_company_history(c.company_name, d, val, 10 + i)

    # 4. Seed Events
    class DummyEvent:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    events = [
        DummyEvent(
            company="Nexus Robotics",
            event_type="Funding",
            title="Nexus Robotics raises $45M Series B for AI expansion",
            published_at=now.isoformat(),
            confidence=0.95,
            impact_score=8.5,
            importance_score=85.0,
            ai_summary="Nexus Robotics secured $45M in Series B funding led by Sequoia to expand their AI manufacturing capabilities.",
            business_impact="Will accelerate go-to-market for their new autonomous factory line.",
            risk_tags='["Execution Risk"]',
            opportunity_tags='["Market Expansion", "Product Innovation"]',
        ),
        DummyEvent(
            company="EcoStream AI",
            event_type="Product Launch",
            title="EcoStream unveils new carbon tracking API",
            published_at=(now - timedelta(hours=5)).isoformat(),
            confidence=0.88,
            impact_score=7.2,
            importance_score=72.0,
            ai_summary="EcoStream AI launched a real-time carbon tracking API aimed at enterprise customers.",
            business_impact="Expected to drive 40% increase in recurring revenue.",
            risk_tags='["Integration Complexity"]',
            opportunity_tags='["B2B Sales"]',
        ),
        DummyEvent(
            company="DataFlow Systems",
            event_type="Layoffs",
            title="DataFlow Systems cuts 15% of workforce amid restructuring",
            published_at=(now - timedelta(days=1)).isoformat(),
            confidence=0.92,
            impact_score=9.0,
            importance_score=90.0,
            ai_summary="DataFlow Systems announced a 15% reduction in force as part of a major restructuring effort.",
            business_impact="Signals significant cash flow issues and operational scaling failures.",
            risk_tags='["Cash Runway", "Talent Drain"]',
            opportunity_tags="[]",
        ),
    ]

    for e in events:
        repo.save_event(e, article_id=None)

    repo.close()
    logger.info("Database seeding complete.")


import subprocess

if __name__ == "__main__":
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    seed_database_if_empty()
