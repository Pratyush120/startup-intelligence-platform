from fastapi import APIRouter, Depends, Query
from typing import Any, List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.pipeline.api_serializer import serialize_strategic_alerts

router = APIRouter(tags=["Alerts"])


@router.get("/alerts", response_model=StandardResponse[List[dict[str, Any]]])
async def get_alerts(
    limit: int = Query(10, ge=1, le=50), repo: Repository = Depends(get_repository)
):
    # Retrieve strategic alerts from DB.
    # For now, we will query events with High/Critical importance.
    # In a full implementation, there might be a strategic_alerts table populated by the pipeline.
    # We do have a strategic_alerts table in schema.py! Let's query it.
    repo.db.execute(
        "SELECT * FROM strategic_alerts WHERE is_active = 1 ORDER BY timestamp DESC LIMIT ?",
        (limit,),
    )
    rows = repo.db.fetchall()

    # If empty, fallback to deriving from high importance events
    if not rows:
        repo.db.execute(
            "SELECT * FROM events WHERE importance_score >= 6.0 ORDER BY published_at DESC LIMIT ?",
            (limit,),
        )
        events = repo.db.fetchall()
        # Map events to alert format
        alerts = []
        for e in events:
            alerts.append(
                {
                    "alert_id": e["event_id"],
                    "title": e["event_type"],
                    "impact": e.get("business_impact", ""),
                    "confidence": e.get("confidence", 0.9),
                    "company_name": e["company_name"],
                    "category": e.get("event_type", "Market Shift"),
                    "recommendation": e.get("ai_summary", ""),
                    "timestamp": e.get("published_at"),
                    "priority": "Critical"
                    if float(e.get("importance_score", 0)) >= 8.0
                    else "High",
                }
            )
        rows = alerts

    serialized = serialize_strategic_alerts(rows)
    return success_response(data=serialized)
