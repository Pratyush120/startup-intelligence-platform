from fastapi import APIRouter, Depends, Query
from typing import Any, List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.pipeline.api_serializer import serialize_recommendations

router = APIRouter(tags=["Recommendations"])


@router.get("/recommendations", response_model=StandardResponse[List[dict[str, Any]]])
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    repo: Repository = Depends(get_repository),
):
    from src.services.intelligence_aggregator import IntelligenceAggregator

    agg = IntelligenceAggregator(repo)
    ctx = await agg.build_global_context("startup investment recommendations")

    recommendations = repo.get_recommendations(limit=limit, offset=offset)

    # Enhance with live aggregator context
    live_news = ctx.get("latest_news", [])
    if live_news:
        recommendations.append(
            {
                "target_entity": live_news[0].title[:50],
                "action_type": "MONITOR",
                "reasoning": f"Live Signal: {live_news[0].snippet}",
                "impact_score": 8.0,
            }
        )

    serialized = serialize_recommendations(recommendations)

    return success_response(
        data=serialized[:limit],
        meta={"limit": limit, "offset": offset, "total": len(serialized)},
    )
