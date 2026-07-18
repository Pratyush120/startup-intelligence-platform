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
    events = repo.get_recent_events(limit=limit, offset=offset, event_type=event_type)

    # serialize_timeline_events natively handles DB rows (dicts)
    serialized = serialize_timeline_events(events)

    return success_response(
        data=serialized,
        meta={
            "limit": limit,
            "offset": offset,
            "event_type": event_type,
            "total": len(serialized),
        },
    )
