"""
Database Seeder - HACKATHON EDITION

Seeds the database with massive, highly realistic data for hackathon demonstrations.
Deletes the old database on run to guarantee a pristine mock state.
"""

import os
import json
from datetime import datetime, timezone, timedelta
from src.database.repository import Repository
from src.utils.logger import get_logger
import subprocess

logger = get_logger(__name__)


def seed_hackathon_data():
    repo = Repository()

    logger.info("Seeding Hackathon Demo Data...")
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    # 1. Seed Market Snapshot
    repo.save_market_snapshot(
        today,
        {
            "funding_amount": 3450000000,  # $3.45B
            "hiring_events": 142,
            "layoff_events": 23,
            "expansion_events": 45,
            "acquisition_events": 12,
            "total_events": 856,
            "market_health": 82.5,
        },
    )

    # 2. Seed Executive Brief
    repo.save_executive_brief(
        {
            "market_health_score": 82.5,
            "investment_climate": "Highly Favorable",
            "risk_level": "Low",
            "growth_outlook": "Accelerating",
            "strategic_summary": "The startup ecosystem is experiencing a massive liquidity event driven by AI infrastructure maturation and DeepTech breakthroughs. Series A rounds have increased by 45% week-over-week.",
            "confidence_score": 0.94,
            "primary_recommendation": "Aggressively allocate capital to generative AI application layers and carbon-capture hardware startups.",
        }
    )

    # 3. Seed Companies
    companies = [
        {"name": "Nexus Robotics", "sector": "Robotics", "momentum": 94, "growth": 88, "risk": 15, "funding": 120_000_000, "rec": "Strong Buy"},
        {"name": "EcoStream AI", "sector": "CleanTech", "momentum": 88, "growth": 91, "risk": 22, "funding": 45_000_000, "rec": "Buy"},
        {"name": "DataFlow Systems", "sector": "SaaS", "momentum": 35, "growth": 20, "risk": 85, "funding": 210_000_000, "rec": "Sell"},
        {"name": "AeroSpace Dynamics", "sector": "SpaceTech", "momentum": 96, "growth": 95, "risk": 40, "funding": 850_000_000, "rec": "Strong Buy"},
        {"name": "FinTrust Bank", "sector": "FinTech", "momentum": 45, "growth": 40, "risk": 60, "funding": 50_000_000, "rec": "Monitor"},
        {"name": "BioSynthetica", "sector": "BioTech", "momentum": 82, "growth": 75, "risk": 35, "funding": 115_000_000, "rec": "Buy"},
        {"name": "QuantumCore", "sector": "DeepTech", "momentum": 98, "growth": 99, "risk": 80, "funding": 320_000_000, "rec": "Strong Buy"},
        {"name": "HealthMatch", "sector": "HealthTech", "momentum": 60, "growth": 65, "risk": 45, "funding": 30_000_000, "rec": "Monitor"},
        {"name": "CyberShield AI", "sector": "Cybersecurity", "momentum": 90, "growth": 85, "risk": 10, "funding": 90_000_000, "rec": "Buy"},
        {"name": "MetaRetail", "sector": "E-Commerce", "momentum": 20, "growth": 15, "risk": 95, "funding": 400_000_000, "rec": "Strong Sell"},
        {"name": "AgriTech Solutions", "sector": "AgriTech", "momentum": 70, "growth": 60, "risk": 25, "funding": 25_000_000, "rec": "Buy"},
        {"name": "NeuroLink Interfaces", "sector": "MedTech", "momentum": 85, "growth": 80, "risk": 50, "funding": 200_000_000, "rec": "Buy"},
        {"name": "UrbanAir Mobility", "sector": "Transportation", "momentum": 75, "growth": 70, "risk": 65, "funding": 150_000_000, "rec": "Monitor"},
        {"name": "EduQuest AI", "sector": "EdTech", "momentum": 55, "growth": 50, "risk": 40, "funding": 15_000_000, "rec": "Monitor"},
        {"name": "SecureLedger", "sector": "Web3", "momentum": 30, "growth": 25, "risk": 88, "funding": 80_000_000, "rec": "Sell"},
        {"name": "SynthMaterials", "sector": "DeepTech", "momentum": 88, "growth": 92, "risk": 30, "funding": 55_000_000, "rec": "Buy"},
        {"name": "CloudNine SaaS", "sector": "SaaS", "momentum": 40, "growth": 35, "risk": 55, "funding": 12_000_000, "rec": "Monitor"},
        {"name": "ZeroCarbon Energy", "sector": "CleanTech", "momentum": 95, "growth": 90, "risk": 18, "funding": 500_000_000, "rec": "Strong Buy"},
        {"name": "OmniLogistics", "sector": "Supply Chain", "momentum": 65, "growth": 60, "risk": 35, "funding": 40_000_000, "rec": "Buy"},
        {"name": "VirtualEstate", "sector": "PropTech", "momentum": 25, "growth": 20, "risk": 90, "funding": 100_000_000, "rec": "Sell"},
    ]

    class DummyCompany:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    for i, c in enumerate(companies):
        comp = DummyCompany(
            company_name=c["name"],
            momentum_score=c["momentum"],
            growth_score=c["growth"],
            risk_score=c["risk"],
            investment_score=min(100, c["momentum"] + 10 - c["risk"] // 5),
            influence_score=c["growth"] - 5,
            business_health=c["momentum"] - 2,
            total_funding=c["funding"],
            recommendation=c["rec"],
        )
        repo.save_company(comp)
        
        # Seed 30 days of history for sparklines
        for d_idx in range(30):
            d = (now - timedelta(days=29 - d_idx)).strftime("%Y-%m-%d")
            base = c["momentum"]
            # Generate realistic curve
            trend_val = base - (29 - d_idx) * 0.5 + (d_idx % 3) * 2 - (d_idx % 5)
            repo.save_company_history(c["name"], d, max(0, min(100, trend_val)), 10 + d_idx)

    # 4. Seed Events
    class DummyEvent:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    events_data = [
        ("Nexus Robotics", "Funding", "Nexus Robotics raises $120M Series C", 0.98, 9.5, 95.0, "Secured $120M in Series C funding to scale their autonomous factory product line.", "Massive acceleration of go-to-market. Competitors will struggle to match capital."),
        ("EcoStream AI", "Product Launch", "EcoStream AI launches Global Carbon Tracker v2", 0.92, 8.2, 82.0, "New product launch offering real-time carbon tracking via satellite data.", "Expected to capture 30% of enterprise market share this year."),
        ("DataFlow Systems", "Layoffs", "DataFlow Systems cuts 25% of workforce", 0.99, 9.8, 98.0, "Announced massive layoffs to preserve cash runway.", "Severe operational distress. Potential bankruptcy risk if they don't pivot."),
        ("AeroSpace Dynamics", "Contract", "AeroSpace Dynamics wins $500M NASA contract", 0.95, 9.9, 99.0, "Awarded exclusive contract to build lunar habitats.", "Guarantees revenue for next 5 years. Massive valuation spike expected."),
        ("FinTrust Bank", "Regulatory", "FinTrust Bank faces SEC probe", 0.88, 8.5, 85.0, "SEC investigating algorithmic trading division for compliance violations.", "Could result in heavy fines and leadership changes."),
        ("BioSynthetica", "Clinical Trial", "BioSynthetica Phase II trials show 95% efficacy", 0.96, 9.2, 92.0, "Breakthrough results in autoimmune disease treatment.", "Paves way for FDA fast-track. High acquisition probability."),
        ("QuantumCore", "Breakthrough", "QuantumCore achieves 1000-qubit coherence", 0.90, 9.6, 96.0, "Major technical milestone in quantum computing stabilization.", "Puts them 2 years ahead of competitors. Strong IP moat."),
        ("HealthMatch", "Partnership", "HealthMatch partners with Mayo Clinic", 0.85, 7.5, 75.0, "Strategic partnership for clinical trial patient matching.", "Validates technology and provides massive data pipeline."),
        ("CyberShield AI", "Funding", "CyberShield AI secures $90M Series B", 0.94, 8.8, 88.0, "Funding led by a16z to expand zero-trust architecture.", "Will aggressive expand into European markets."),
        ("MetaRetail", "Earnings Miss", "MetaRetail misses Q3 targets by 40%", 0.99, 9.4, 94.0, "Catastrophic revenue miss due to failing VR storefronts.", "Significant structural failure in core business model."),
        ("AgriTech Solutions", "Expansion", "AgriTech Solutions enters South American market", 0.82, 7.0, 70.0, "Expanding precision farming software globally.", "Opens up $5B total addressable market."),
        ("NeuroLink Interfaces", "FDA Approval", "NeuroLink receives FDA clearance for human trials", 0.97, 9.7, 97.0, "Regulatory green light for brain-computer interface implant.", "Transforms company from speculative to clinical-stage."),
        ("SecureLedger", "Hack", "SecureLedger loses $50M in smart contract exploit", 0.99, 9.9, 99.0, "Major security breach draining user funds.", "Existential threat. Massive loss of customer trust."),
        ("SynthMaterials", "Patent", "SynthMaterials granted patent for biodegradable plastic", 0.89, 7.8, 78.0, "Key IP secured for core material science technology.", "Strengthens competitive moat against incumbents."),
        ("ZeroCarbon Energy", "Funding", "ZeroCarbon Energy closes $500M mega-round", 0.98, 9.8, 98.0, "Massive funding to build direct air capture facilities.", "Establishes them as the market leader in carbon removal."),
    ]

    for i, ed in enumerate(events_data):
        e = DummyEvent(
            company=ed[0],
            event_type=ed[1],
            title=ed[2],
            published_at=(now - timedelta(hours=i*2)).isoformat(),
            confidence=ed[3],
            impact_score=ed[4],
            importance_score=ed[5],
            ai_summary=ed[6],
            business_impact=ed[7],
            risk_tags='["Execution Risk"]' if ed[4] < 8 else '[]',
            opportunity_tags='["Market Capture"]' if ed[4] >= 8 else '[]',
        )
        repo.save_event(e, article_id=None)

    # 5. Seed Premium Recommendations (Reports)
    recommendations = [
        {
            "title": "Quantum Computing Maturation: Accumulate QuantumCore",
            "reason": "QuantumCore's recent 1000-qubit coherence breakthrough fundamentally shifts the timelines for commercial quantum utility. They are now positioned 24-36 months ahead of legacy tech giants.",
            "priority": "High",
            "confidence": 0.92,
            "evidence_score": 96.0,
            "strategic_impact": "Early accumulation will capture the premium of the upcoming commercialization phase.",
            "opportunity_est": "$45B Total Addressable Market (TAM) by 2030",
            "risk_est": "Moderate risk of scaling hardware constraints",
            "suggested_action": "Allocate 15% of DeepTech portfolio to QuantumCore. Initiate talks for secondary market shares.",
            "evidence": [
                "Achieved 1000-qubit coherence on Nov 12, validated by independent researchers.",
                "Secured 4 new patents blocking alternative architectures.",
                "Competitors (IBM, Google) are reporting delays in error-correction models."
            ],
            "related_companies": ["QuantumCore"],
            "related_event_ids": [7]
        },
        {
            "title": "SaaS Sector Contagion: Liquidate DataFlow Systems",
            "reason": "DataFlow Systems is exhibiting classic signs of irreversible operational distress. A 25% reduction in workforce paired with a 70% drop in momentum score indicates failed product-market fit at scale.",
            "priority": "Critical",
            "confidence": 0.98,
            "evidence_score": 99.0,
            "strategic_impact": "Prevent capital destruction. Reallocate to high-momentum AI infrastructure.",
            "opportunity_est": "Capital preservation of $210M invested capital",
            "risk_est": "Extremely high bankruptcy probability within 8 months",
            "suggested_action": "Immediately liquidate positions. Short if market mechanisms allow. Cut all strategic partnerships.",
            "evidence": [
                "Announced 25% workforce reduction across core engineering teams.",
                "Customer churn increased by 40% QoQ according to alt-data scraping.",
                "Momentum score collapsed from 85 to 35 in just 30 days."
            ],
            "related_companies": ["DataFlow Systems", "CloudNine SaaS"],
            "related_event_ids": [3]
        },
        {
            "title": "Carbon Capture Infrastructure: Buy ZeroCarbon Energy",
            "reason": "The closing of a $500M mega-round combined with accelerating regulatory mandates makes ZeroCarbon the undeniable front-runner in direct air capture. The capital acts as an insurmountable moat.",
            "priority": "High",
            "confidence": 0.95,
            "evidence_score": 94.0,
            "strategic_impact": "Establish anchor position in the emerging trillion-dollar climate compliance market.",
            "opportunity_est": "15x multiple potential over 5-year horizon",
            "risk_est": "Low risk of capital failure, medium risk of execution delay",
            "suggested_action": "Participate heavily in upcoming syndicates. Monitor for aggressive M&A strategy.",
            "evidence": [
                "$500M funding round closed led by sovereign wealth funds.",
                "EU regulatory mandates announced requiring 20% offset by 2030.",
                "Momentum score leads the entire CleanTech sector at 95."
            ],
            "related_companies": ["ZeroCarbon Energy", "EcoStream AI"],
            "related_event_ids": [15]
        },
        {
            "title": "Web3 Security Crisis: Short SecureLedger",
            "reason": "A $50M smart contract exploit fundamentally breaks the trust model required for SecureLedger's B2B enterprise product. Institutional clients are legally required to offboard.",
            "priority": "Critical",
            "confidence": 0.99,
            "evidence_score": 99.5,
            "strategic_impact": "Total collapse of primary revenue streams.",
            "opportunity_est": "N/A",
            "risk_est": "Existential risk - 95% probability of total failure",
            "suggested_action": "Exit entirely. Use as a case study to mandate zero-trust architecture audits for all portfolio companies.",
            "evidence": [
                "$50M exploit confirmed on mainnet.",
                "Risk score spiked to 88 (Maximum Alert).",
                "Growth score collapsed to 25."
            ],
            "related_companies": ["SecureLedger", "CyberShield AI"],
            "related_event_ids": [13]
        }
    ]

    repo.save_recommendations(recommendations)

    repo.close()
    logger.info("Hackathon Database Seeding Complete!")


if __name__ == "__main__":
    from config.config import Config
    db_path = Config.DATABASE_PATH
    if os.path.exists(db_path):
        logger.info(f"Found existing database at {db_path}. Deleting to reset for hackathon demo...")
        os.remove(db_path)
    
    # Run Alembic migrations to create tables
    logger.info("Running database migrations...")
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    
    seed_hackathon_data()
