from fastapi import APIRouter, Depends
from typing import Any
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository

router = APIRouter(tags=["Executive"])


@router.get("/executive-brief", response_model=StandardResponse[dict[str, Any]])
async def get_executive_brief(repo: Repository = Depends(get_repository)):
    from src.services.intelligence_aggregator import IntelligenceAggregator

    agg = IntelligenceAggregator(repo)
    ctx = await agg.build_global_context("technology startup market health")

    brief = repo.get_latest_executive_brief()
    if not brief:
        # Fallback empty brief if pipeline never ran
        brief = {
            "id": "empty",
            "date": "",
            "market_health_score": 50,
            "investment_climate": "Neutral",
            "risk_level": "Medium",
            "growth_outlook": "Stable",
            "strategic_summary": "Initial intelligence gathered.",
            "confidence_score": 50,
            "primary_recommendation": "Monitor market trends.",
        }

    # Enhance summary with live context
    live_news = ctx.get("latest_news", [])
    if live_news:
        brief["strategic_summary"] += (
            f"\n\nLive Market Signal: {live_news[0].title} - {live_news[0].snippet[:100]}..."
        )

    return success_response(
        data={
            "id": brief.get("id", "latest"),
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
