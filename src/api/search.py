from fastapi import APIRouter, Depends, Query
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
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
    companies = repo.search_entities(query=q, limit=limit, offset=offset)
    events = repo.search_events(query=q, limit=limit, offset=offset)

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

    # Fetch real-time data from DuckDuckGo for live internet search
    try:
        from duckduckgo_search import DDGS
        from datetime import datetime, timezone

        ddgs = DDGS()
        news_results = list(
            ddgs.news(
                keywords=f"{q} startup OR company OR tech OR business", max_results=3
            )
        )
        for nr in news_results:
            events.append(
                {
                    "company_name": q.title(),
                    "title": nr.get("title", ""),
                    "event_type": "Live News",
                    "published_at": nr.get(
                        "date", datetime.now(timezone.utc).isoformat()
                    ),
                    "business_impact": nr.get("body", "")[:200],
                    "ai_summary": nr.get("source", ""),
                    "importance_score": 7.0,
                }
            )
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")

    serialized_events = serialize_timeline_events(events)

    return success_response(
        data={"companies": serialized_companies, "events": serialized_events},
        meta={"query": q, "limit": limit, "offset": offset},
    )
