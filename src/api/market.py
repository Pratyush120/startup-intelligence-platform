from fastapi import APIRouter, Depends
from typing import Any, List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.pipeline.api_serializer import serialize_market_snapshots

router = APIRouter(tags=["Market"])


@router.get("/market-snapshot", response_model=StandardResponse[List[dict[str, Any]]])
async def get_market_snapshot(repo: Repository = Depends(get_repository)):
    from src.services.intelligence_aggregator import IntelligenceAggregator

    agg = IntelligenceAggregator(repo)
    ctx = await agg.build_global_context("technology market snapshot trends")

    snapshot = repo.get_latest_market_snapshot()
    if not snapshot:
        snapshot = {
            "snapshot_date": "",
            "total_companies_tracked": 0,
            "total_events_tracked": 0,
            "hot_sectors": "",
            "emerging_startups": "",
        }

    # Enhance with live news/trends
    live_news = ctx.get("latest_news", [])
    if live_news:
        snapshot["hot_sectors"] = (
            f"Live Signal: {live_news[0].title} | {snapshot.get('hot_sectors', '')}"
        )

    serialized = serialize_market_snapshots([snapshot])
    return success_response(data=serialized)
