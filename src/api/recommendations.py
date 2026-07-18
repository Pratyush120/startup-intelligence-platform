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
    recommendations = repo.get_recommendations(limit=limit, offset=offset)
    serialized = serialize_recommendations(recommendations)

    return success_response(
        data=serialized,
        meta={"limit": limit, "offset": offset, "total": len(serialized)},
    )
