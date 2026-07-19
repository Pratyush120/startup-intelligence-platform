from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any, List
from src.api.response import StandardResponse, success_response, error_response
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
    request: CopilotRequest,
    repo: Repository = Depends(get_repository)
):
    try:
        analyzer = LLMAnalyzer()
        
        # We need a proper analysis from the LLM based on the prompt.
        # We'll adapt LLMAnalyzer to just generate a response if it were a direct chat,
        # but for now we'll do a mock or use the LLMAnalyzer's analyze method.
        # Since analyze() expects title/desc, we'll wrap the prompt.
        
        # Real implementation using the analyzer:
        analysis = analyzer.analyze(
            title="User Query",
            description=request.prompt,
            event_type="Strategic Inquiry",
            company="Market"
        )
        
        return success_response(
            data=CopilotResponse(
                role="assistant",
                content=analysis.executive_summary,
                cersr=CERSRResponse(
                    confidence=int(analysis.confidence * 100),
                    evidence=analysis.business_impact,
                    sources=["Intelligence Database", "Live Pipeline"],
                    reasoning=analysis.key_insight,
                    strategy=analysis.strategic_recommendation
                )
            ).model_dump()
        )
    except Exception as e:
        return success_response(
            data=CopilotResponse(
                role="assistant",
                content=f"Error generating strategic analysis: {str(e)}",
            ).model_dump()
        )
