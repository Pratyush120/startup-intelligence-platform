import time
from fastapi import APIRouter, Depends
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository

router = APIRouter(tags=["Health"])
start_time = time.time()


@router.get("/health", response_model=StandardResponse[dict[str, Any]])
async def health_check(repo: Repository = Depends(get_repository)):
    try:
        # Check database connection
        repo.db.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "error"

    status = {
        "database": db_status,
        "pipeline": "ready",
        "llm_provider": "configured",
        "collectors": ["NewsAPI", "GoogleNews", "Mock"],
        "application_version": "1.0.0",
        "uptime_seconds": int(time.time() - start_time),
    }

    return success_response(data=status)
