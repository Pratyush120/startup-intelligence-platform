import os
import asyncio
from celery import Celery
from src.pipeline.orchestrator import PipelineOrchestrator
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Use environment variable for broker, fallback to local Redis
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

app = Celery(
    "sdip",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL,
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
)


def _run_pipeline_sync():
    """Wrapper to run the async pipeline orchestrator in a sync context."""
    logger.info("Starting SDIP pipeline via Celery...")
    orchestrator = PipelineOrchestrator()

    # Run the async pipeline inside an event loop
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    result = loop.run_until_complete(orchestrator.run())
    logger.info("Pipeline completed successfully via Celery.")
    return result


@app.task(name="src.worker.run_pipeline_task", bind=True)
def run_pipeline_task(self):
    """
    Executes the full SDIP pipeline asynchronously.
    """
    try:
        result = _run_pipeline_sync()
        return result
    except Exception as e:
        logger.error("Pipeline failed in Celery worker", exc_info=True)
        raise e
