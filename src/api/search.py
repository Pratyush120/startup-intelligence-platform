from fastapi import APIRouter, Depends, Query
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.services.intelligence_aggregator import IntelligenceAggregator
from src.pipeline.api_serializer import (
    serialize_company_metrics,
    serialize_timeline_events,
)

router = APIRouter(tags=["Search"])


class CompanyProxy:
    def __init__(self, data: dict):
        for k, v in data.items():
            setattr(self, k, v)


@router.get("/search", response_model=StandardResponse[dict[str, Any]])
async def search(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    repo: Repository = Depends(get_repository),
):
    aggregator = IntelligenceAggregator(repo)
    global_context = await aggregator.build_global_context(q)

    # Convert db dictionary to list format expected by serializer
    db_company = global_context.get("company", {})
    companies = (
        [db_company]
        if isinstance(db_company, dict) and "company_name" in db_company
        else []
    )

    events = global_context.get("db_events", [])
    latest_news = global_context.get("latest_news", [])

    company_proxies = []
    sparklines = {}
    for c in companies:
        c_name = c.get("company_name", q)
        company_proxies.append(CompanyProxy(c))
        history = repo.get_company_history(c_name)
        if not history:
            history = [c.get("business_health", 50.0)]
        if len(history) < 5:
            history = history + [history[-1]] * (5 - len(history))
        sparklines[c_name] = history[-5:]

    serialized_companies = serialize_company_metrics(company_proxies, sparklines)

    # Blend aggregated news into events
    for n in latest_news:
        events.append(
            {
                "company_name": q.title(),
                "title": n.title,
                "event_type": f"Live News ({n.source.provider})",
                "published_at": n.published_at,
                "business_impact": n.snippet[:200],
                "ai_summary": n.publisher,
                "importance_score": 7.0,
            }
        )

    serialized_events = serialize_timeline_events(events)

    return success_response(
        data={"companies": serialized_companies, "events": serialized_events},
        meta={"query": q, "limit": limit, "offset": offset},
    )
