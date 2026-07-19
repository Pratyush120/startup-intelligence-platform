from fastapi import APIRouter, Depends, Query
from typing import Any, List, Optional
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.pipeline.api_serializer import serialize_timeline_events

router = APIRouter(tags=["Timeline"])


@router.get("/timeline", response_model=StandardResponse[List[dict[str, Any]]])
async def get_timeline(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    event_type: Optional[str] = None,
    repo: Repository = Depends(get_repository),
):
    from src.services.intelligence_aggregator import IntelligenceAggregator
    events = repo.get_recent_events(limit=limit, offset=offset, event_type=event_type)

    agg = IntelligenceAggregator(repo)
    global_ctx = await agg.build_global_context("startup funding news")
    
    live_news = global_ctx.get("latest_news", [])
    for n in live_news:
        events.append(
            {
                "company_name": "Industry",
                "title": n.title,
                "event_type": f"Live News ({n.source.provider})",
                "published_at": n.published_at,
                "business_impact": n.snippet[:200],
                "ai_summary": n.publisher,
                "importance_score": 8.0,
            }
        )

    # Sort combined events by published_at (descending)
    def parse_date(e):
        return e.get("published_at", "")
    events.sort(key=parse_date, reverse=True)

    serialized = serialize_timeline_events(events[:limit])

    return success_response(
        data=serialized,
        meta={
            "limit": limit,
            "offset": offset,
            "event_type": event_type,
            "total": len(serialized),
        },
    )
