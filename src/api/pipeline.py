from fastapi import APIRouter, Depends
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.worker import run_pipeline_task
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["Pipeline"])


@router.post("/pipeline/run", response_model=StandardResponse[dict[str, str]])
async def run_pipeline():
    task = run_pipeline_task.delay()
    return success_response(
        data={"message": "Pipeline execution started via Celery.", "task_id": task.id},
        meta={"status": "running"},
    )


@router.get("/pipeline/status", response_model=StandardResponse[dict[str, Any]])
async def get_pipeline_status(repo: Repository = Depends(get_repository)):
    run = repo.get_latest_pipeline_run()
    if not run:
        return success_response(
            data={"status": "unknown", "message": "No pipeline runs found."}
        )

    return success_response(data=run)
