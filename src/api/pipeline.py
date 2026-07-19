from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["Pipeline"])
@router.post("/pipeline/run", response_model=StandardResponse[dict[str, str]])
async def run_pipeline(background_tasks: BackgroundTasks, repo: Repository = Depends(get_repository)):
    from src.pipeline.orchestrator import PipelineOrchestrator
    
    def execute_pipeline():
        try:
            orchestrator = PipelineOrchestrator()
            orchestrator.run()
        except Exception as e:
            logger.error(f"Background pipeline execution failed: {e}")

    background_tasks.add_task(execute_pipeline)
    
    return success_response(
        data={"message": "Pipeline execution started in background.", "task_id": "local-bg-task"},
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
