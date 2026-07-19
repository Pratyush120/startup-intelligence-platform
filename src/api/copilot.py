from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.pipeline.llm_analyzer import LLMAnalyzer

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
        analyzer = LLMAnalyzer()

        # Query the database to find actual matching intelligence
        companies = repo.search_entities(request.prompt, limit=3)
        events = repo.search_events(request.prompt, limit=5)

        if not companies and not events:
            return success_response(
                data=CopilotResponse(
                    role="assistant",
                    content=f"I couldn't find any specific intelligence on '{request.prompt}' in our current database. Please try another query or run the pipeline to gather more data.",
                ).model_dump()
            )

        # Build context from database results
        context_lines = []
        if companies:
            context_lines.append("Matching Companies:")
            for c in companies:
                context_lines.append(
                    f"- {c['company_name']} (Health: {c.get('business_health', 0)}, Momentum: {c.get('momentum_score', 0)})"
                )
        if events:
            context_lines.append("\nRecent Events:")
            for e in events:
                context_lines.append(f"- {e['title']}")

        context_str = "\n".join(context_lines)

        # Analyze using the LLM/Heuristic provider
        analysis = analyzer.analyze(
            title=request.prompt,
            description=context_str,
            event_type="Strategic Inquiry",
            company="Various" if len(companies) != 1 else companies[0]["company_name"],
        )

        final_response = f"Based on our intelligence database:\n\n{analysis.executive_summary}\n\n{context_str}"

        return success_response(
            data=CopilotResponse(
                role="assistant",
                content=final_response,
                cersr=CERSRResponse(
                    confidence=int(analysis.confidence * 100),
                    evidence=analysis.business_impact,
                    sources=["Intelligence Database"],
                    reasoning=analysis.key_insight,
                    strategy=analysis.strategic_recommendation,
                ),
            ).model_dump()
        )
    except Exception as e:
        return success_response(
            data=CopilotResponse(
                role="assistant",
                content=f"Error generating strategic analysis: {str(e)}",
            ).model_dump()
        )
