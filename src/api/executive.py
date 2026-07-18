from fastapi import APIRouter, Depends
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository

router = APIRouter(tags=["Executive"])


@router.get("/executive-brief", response_model=StandardResponse[dict[str, Any]])
async def get_executive_brief(repo: Repository = Depends(get_repository)):
    brief = repo.get_latest_executive_brief()
    if not brief:
        # Fallback empty brief if pipeline never ran
        brief = {
            "id": "empty",
            "date": "",
            "marketHealthScore": 0,
            "investmentClimate": "Neutral",
            "riskLevel": "Low",
            "growthOutlook": "Stable",
            "strategicSummary": "No data available. Run pipeline first.",
            "confidenceScore": 0,
            "primaryRecommendation": "N/A",
        }
        return success_response(data=brief)

    # Re-map DB snake_case columns back to camelCase frontend schema
    return success_response(
        data={
            "id": "latest",
            "date": brief.get("generated_at", ""),
            "marketHealthScore": brief.get("market_health_score", 0),
            "investmentClimate": brief.get("investment_climate", "Neutral"),
            "riskLevel": brief.get("risk_level", "Medium"),
            "growthOutlook": brief.get("growth_outlook", "Stable"),
            "strategicSummary": brief.get("strategic_summary", ""),
            "confidenceScore": brief.get("confidence_score", 0),
            "primaryRecommendation": brief.get("primary_recommendation", ""),
        }
    )
