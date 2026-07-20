from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.services.intelligence_aggregator import IntelligenceAggregator
from src.services.providers.gemini_provider import GeminiProvider

router = APIRouter(tags=["Copilot"])


class CopilotRequest(BaseModel):
    prompt: str


class CERSRResponse(BaseModel):
    confidence: int
    evidence: str
    sources: List[str]
    reasoning: str
    strategy: str


class CopilotResponse(BaseModel):
    role: str
    content: str
    cersr: CERSRResponse | None = None


@router.post("/copilot/chat", response_model=StandardResponse[CopilotResponse])
async def chat_copilot(
    request: CopilotRequest, repo: Repository = Depends(get_repository)
):
    try:
        # 1. Unified Intelligence Aggregator Context
        aggregator = IntelligenceAggregator(repo)
        global_context = await aggregator.build_global_context(request.prompt)

        # 2. Call Gemini
        provider = GeminiProvider()

        # 3. Analyze
        analysis = provider.analyze_strategic_context(
            context_data=global_context, user_prompt=request.prompt
        )

        # 4. Format for Frontend
        content = f"**Executive Summary**\n{analysis.summary}\n\n"
        if analysis.key_insights:
            content += (
                "**Key Insights**\n"
                + "\n".join(f"- {i}" for i in analysis.key_insights)
                + "\n\n"
            )
        if analysis.recommendations:
            content += (
                "**Recommendations**\n"
                + "\n".join(f"- {r}" for r in analysis.recommendations)
                + "\n\n"
            )

        cersr = CERSRResponse(
            confidence=int(analysis.confidence * 100)
            if analysis.confidence <= 1.0
            else int(analysis.confidence),
            evidence=" | ".join(analysis.opportunities + analysis.risks)[:200],
            sources=analysis.sources
            if analysis.sources
            else ["Intelligence Aggregator"],
            reasoning=analysis.competitor_perspective or "Synthesized strategic data.",
            strategy="Gemini AI Analysis",
        )

        return success_response(
            data=CopilotResponse(
                role="assistant", content=content.strip(), cersr=cersr
            ).model_dump()
        )
    except Exception as e:
        return success_response(
            data=CopilotResponse(
                role="assistant",
                content=f"Error generating strategic analysis: {str(e)}",
            ).model_dump()
        )
