from fastapi import APIRouter, Depends
from typing import Any, List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.pipeline.api_serializer import serialize_market_snapshots

router = APIRouter(tags=["Market"])


@router.get("/market-snapshot", response_model=StandardResponse[List[dict[str, Any]]])
async def get_market_snapshot(repo: Repository = Depends(get_repository)):
    snapshot = repo.get_latest_market_snapshot()
    if not snapshot:
        return success_response(data=[])

    # serialize expects a list of dicts
    serialized = serialize_market_snapshots([snapshot])
    return success_response(data=serialized)
