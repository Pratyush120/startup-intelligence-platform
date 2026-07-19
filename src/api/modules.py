from fastapi import APIRouter, Depends
from typing import Any, List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository

router = APIRouter(tags=["Modules"])


@router.get("/modules", response_model=StandardResponse[List[dict[str, Any]]])
async def get_modules(repo: Repository = Depends(get_repository)):
    brief = repo.get_latest_executive_brief()
    if not brief:
        return success_response(data=[])

    modules = [
        {
            "id": brief.get("brief_id", "latest"),
            "question": "What is the strategic summary?",
            "answer": brief.get("strategic_summary", ""),
            "evidence": [],
            "confidence": brief.get("confidence_score", 0.0),
            "action": {
                "label": brief.get("primary_recommendation", "Review"),
                "intent": "Review",
            },
        }
    ]
    return success_response(data=modules)
