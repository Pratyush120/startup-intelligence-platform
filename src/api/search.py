from fastapi import APIRouter, Depends, Query
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.knowledge.store import KnowledgeStore
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
    store = KnowledgeStore(repo)
    global_context = store.search_global(q)

    companies = global_context.get("companies", [])
    events = global_context.get("events", [])
    live_news = global_context.get("live_news", [])

    company_proxies = []
    sparklines = {}
    for c in companies:
        c_name = c["company_name"]
        company_proxies.append(CompanyProxy(c))
        history = repo.get_company_history(c_name)
        if not history:
            history = [c.get("business_health", 50.0)]
        if len(history) < 5:
            history = history + [history[-1]] * (5 - len(history))
        sparklines[c_name] = history[-5:]

    serialized_companies = serialize_company_metrics(company_proxies, sparklines)

    # Blend SERP live_news into events
    for nr in live_news:
        events.append(
            {
                "company_name": q.title(),
                "title": nr.get("title", ""),
                "event_type": "Live SERP News",
                "published_at": nr.get("published_at", ""),
                "business_impact": nr.get("snippet", "")[:200],
                "ai_summary": nr.get("publisher", ""),
                "importance_score": 7.0,
            }
        )

    serialized_events = serialize_timeline_events(events)

    return success_response(
        data={"companies": serialized_companies, "events": serialized_events},
        meta={"query": q, "limit": limit, "offset": offset},
    )
