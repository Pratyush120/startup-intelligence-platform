from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository

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
        # Query the database to find actual matching intelligence
        companies = repo.search_entities(request.prompt, limit=3)
        events = repo.search_events(request.prompt, limit=5)

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
        if not context_str:
            context_str = "No specific data found in internal database."

        # Fetch real conversational response from g4f chat
        try:
            from g4f.client import Client

            client = Client()
            prompt = f"User asks: {request.prompt}\n\nInternal Data Context:\n{context_str}\n\nProvide a helpful, conversational strategic analysis addressing the user's prompt using the context provided if relevant, or external knowledge if not."
            chat_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            chat_response = chat_completion.choices[0].message.content
        except Exception as e:
            chat_response = (
                f"I'm sorry, I encountered an issue generating a response: {str(e)}"
            )

        return success_response(
            data=CopilotResponse(
                role="assistant",
                content=chat_response,
                cersr=CERSRResponse(
                    confidence=85,
                    evidence="Synthesized from internal data and external knowledge.",
                    sources=["Intelligence Database", "Live Web Knowledge"],
                    reasoning="Strategic synthesis of available contexts.",
                    strategy="Monitor for upcoming shifts based on user query.",
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
