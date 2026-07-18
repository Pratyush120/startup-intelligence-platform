"""
API Serializer

Converts internal Python intelligence models into JSON-serializable dicts
that exactly match the frontend TypeScript interfaces defined in:
  frontend/src/lib/types/executive.ts

This is the single source of truth for the API contract.
If the TypeScript interface changes, update this file accordingly.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, List


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ===========================================================================
# Executive Brief
# Matches: ExecutiveBrief (TypeScript)
# ===========================================================================

def serialize_executive_brief(
    brief_id: str,
    market_health_score: float,
    investment_climate: str,
    risk_level: str,
    growth_outlook: str,
    strategic_summary: str,
    confidence_score: float,
    primary_recommendation: str,
) -> dict[str, Any]:
    """
    Output matches ExecutiveBrief TypeScript interface exactly.
    """
    return {
        "id": str(brief_id),
        "date": _now_iso(),
        "marketHealthScore": round(market_health_score, 1),
        "investmentClimate": investment_climate,   # "Favorable" | "Neutral" | "Hostile"
        "riskLevel": risk_level,                    # "Critical" | "High" | "Medium" | "Low"
        "growthOutlook": growth_outlook,            # "Accelerating" | "Stable" | "Decelerating"
        "strategicSummary": strategic_summary,
        "confidenceScore": round(confidence_score * 100, 1),
        "primaryRecommendation": primary_recommendation,
    }


# ===========================================================================
# Metric Cards
# Matches: MetricCard[] (TypeScript)
# ===========================================================================

def serialize_metric_cards(
    total_companies: int,
    funding_today: float,
    total_events: int,
    market_health: float,
    avg_confidence: float,
    companies_sparkline: List[float],
    funding_sparkline: List[float],
    events_sparkline: List[float],
    health_sparkline: List[float],
) -> List[dict[str, Any]]:
    """
    Produces the 4 primary MetricCard objects for the frontend MetricGrid.
    """
    funding_b = round(funding_today / 1_000_000_000, 2)

    return [
        {
            "id": "m_companies",
            "label": "Companies Tracked",
            "value": f"{total_companies:,}",
            "trend": 1.2,           # Placeholder — calculate from history in future
            "trendLabel": "vs last week",
            "sparkline": companies_sparkline,
            "iconType": "Building",
        },
        {
            "id": "m_funding",
            "label": "Funding Tracked Today",
            "value": f"${funding_b}B" if funding_today >= 1e9 else f"${round(funding_today/1e6, 0):.0f}M",
            "trend": 0.0,
            "trendLabel": "vs 30d avg",
            "sparkline": funding_sparkline,
            "iconType": "DollarSign",
        },
        {
            "id": "m_events",
            "label": "Business Events",
            "value": str(total_events),
            "trend": 0.0,
            "trendLabel": "vs yesterday",
            "sparkline": events_sparkline,
            "iconType": "Activity",
        },
        {
            "id": "m_confidence",
            "label": "Intelligence Confidence",
            "value": f"{round(avg_confidence * 100, 0):.0f}%",
            "trend": 0.5,
            "trendLabel": "vs yesterday",
            "sparkline": health_sparkline,
            "iconType": "BrainCircuit",
        },
    ]


# ===========================================================================
# Company Metrics (Top Companies Table)
# Matches: CompanyMetric[] (TypeScript)
# ===========================================================================

def serialize_company_metrics(
    companies: List[Any],
    sparklines: dict[str, List[float]],
) -> List[dict[str, Any]]:
    """
    Args:
        companies: List of CompanyIntelligence objects from the analytics engine.
        sparklines: Dict mapping company_name → 5-point sparkline list.

    Returns list matching CompanyMetric TypeScript interface.
    """
    result = []
    for c in companies:
        name = c.company_name
        health = getattr(c, "business_health", 50.0)
        trend = "up" if health >= 70 else ("down" if health < 40 else "flat")

        result.append({
            "id": f"c_{name.lower().replace(' ', '_')}",
            "name": name,
            "momentum": round(getattr(c, "momentum_score", 0), 0),
            "fundingTotal": getattr(c, "total_funding", 0),
            "growthScore": round(getattr(c, "growth_score", 0), 0),
            "riskScore": round(getattr(c, "risk_score", 0), 0),
            "recommendation": getattr(c, "recommendation", "Monitor"),
            "trendDirection": trend,
            "sparklineData": sparklines.get(name, [50.0] * 5),
        })
    return result


# ===========================================================================
# Market Snapshots (Area Chart)
# Matches: MarketSnapshot[] (TypeScript)
# ===========================================================================

def serialize_market_snapshots(
    rows: List[dict[str, Any]],
) -> List[dict[str, Any]]:
    """
    Args:
        rows: List of dicts with keys:
              date, funding_amount, hiring_events, layoff_events.
    """
    return [
        {
            "date": row["date"],
            "fundingAmount": round(row.get("funding_amount", 0) / 1_000_000, 2),  # → $M
            "hiringEvents": row.get("hiring_events", 0),
            "layoffEvents": row.get("layoff_events", 0),
        }
        for row in rows
    ]


# ===========================================================================
# Strategic Alerts
# Matches: StrategicAlert[] (TypeScript)
# ===========================================================================

def serialize_strategic_alerts(
    rows: List[dict[str, Any]],
) -> List[dict[str, Any]]:
    return [
        {
            "id": f"sa_{row['alert_id']}",
            "title": row["title"],
            "impact": row.get("impact", ""),
            "confidence": round(float(row.get("confidence", 0.7)) * 100, 0),
            "companyName": row.get("company_name"),
            "category": row.get("category", "Market Shift"),
            "recommendation": row.get("recommendation", ""),
            "timestamp": row.get("timestamp", _now_iso()),
            "priority": row.get("priority", "Medium"),
        }
        for row in rows
    ]


# ===========================================================================
# Timeline Events
# Matches: TimelineEvent[] (TypeScript)
# ===========================================================================

def serialize_timeline_events(
    events: List[Any],
) -> List[dict[str, Any]]:
    """
    Args:
        events: List of BusinessEvent objects or DB row dicts.
    """
    result = []
    for e in events:
        # Support both objects (from engine) and dicts (from DB rows)
        if isinstance(e, dict):
            company = e.get("company_name", "Unknown")
            event_type = e.get("event_type", "General")
            published = e.get("published_at", _now_iso())
            impact = e.get("business_impact") or e.get("title", "")
            summary = e.get("ai_summary") or impact
            importance_score = float(e.get("importance_score", 5.0))
        else:
            company = getattr(e, "company", "Unknown")
            event_type = getattr(e, "event_type", "General")
            published = getattr(e, "published_at", _now_iso())
            impact = getattr(e, "title", "")
            summary = impact
            importance_score = float(getattr(e, "impact_score", 5.0))

        if importance_score >= 8.0:
            importance = "Critical"
        elif importance_score >= 6.0:
            importance = "High"
        elif importance_score >= 4.0:
            importance = "Medium"
        else:
            importance = "Low"

        result.append({
            "id": f"te_{id(e)}",
            "companyName": company,
            "eventType": event_type,
            "date": str(published) if published else _now_iso(),
            "importance": importance,
            "businessImpact": impact,
            "aiSummary": summary,
        })
    return result


# ===========================================================================
# AI Recommendations
# Matches: Recommendation[] (TypeScript)
# ===========================================================================

def serialize_recommendations(
    rows: List[dict[str, Any]],
) -> List[dict[str, Any]]:
    return [
        {
            "id": f"r_{row['rec_id']}",
            "title": row["title"],
            "reason": row.get("reason", ""),
            "evidence": json.loads(row.get("evidence_list", "[]")),
            "confidence": round(float(row.get("confidence", 0.7)) * 100, 0),
            "suggestedAction": row.get("suggested_action", ""),
            "priority": row.get("priority", "Medium"),
            "strategicImpact": row.get("strategic_impact", ""),
            "estimatedOpportunity": row.get("opportunity_est", ""),
            "estimatedRisk": row.get("risk_est", ""),
            "timestamp": row.get("generated_at", _now_iso()),
            "evidenceScore": round(float(row.get("evidence_score", 70.0)), 0),
            "relatedCompanies": json.loads(row.get("related_companies", "[]")),
            "relatedEvents": json.loads(row.get("related_event_ids", "[]")),
        }
        for row in rows
    ]
