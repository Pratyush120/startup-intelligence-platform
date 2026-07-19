import os
import json
from typing import Optional
from pydantic import ValidationError
from google import genai

from src.models.intelligence import CopilotResponse
from src.utils.logger import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)

class EventAnalysisResponse(BaseModel):
    executive_summary: str = ""
    business_impact: str = ""
    strategic_recommendation: str = ""
    risk: str = ""
    opportunity: str = ""
    key_insight: str = ""
    confidence: float = 0.75
    prompt_version: str = "v1"
    token_usage: int = 0
    processing_time_ms: int = 0

class GeminiProvider:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Configuration Error: GEMINI_API_KEY environment variable is required.")
        
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Client: {e}")
            raise

    def analyze_strategic_context(self, context_text: str, user_prompt: str) -> CopilotResponse:
        system_instruction = (
            "You are the Strategic Decision Intelligence Copilot.\n\n"
            "You help executives, investors, analysts and founders.\n\n"
            "Always provide:\n"
            "Executive Summary\n"
            "Key Insights\n"
            "Risks\n"
            "Opportunities\n"
            "Competitor Perspective\n"
            "Strategic Recommendation\n"
            "Confidence Level\n"
            "Sources Used"
        )
        
        full_prompt = f"Context:\n{context_text}\n\nUser Question:\n{user_prompt}"

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=CopilotResponse,
                    temperature=0.4,
                )
            )
            
            json_str = response.text
            if not json_str:
                raise RuntimeError("Empty response from Gemini")
                
            parsed = json.loads(json_str)
            return CopilotResponse(**parsed)
            
        except ValidationError as e:
            logger.error(f"Failed to parse Gemini structured response: {e}")
            raise RuntimeError(f"Gemini API returned malformed data: {e}")
        except Exception as e:
            logger.error(f"Gemini API request failed: {e}")
            raise RuntimeError(f"Gemini API failure: {e}")
            
    def analyze_event(self, title: str, description: str, event_type: str, company: str) -> EventAnalysisResponse:
        system_instruction = (
            "You are a senior investment analyst. Analyze this startup news event.\n"
            "Return a JSON object with: executive_summary, business_impact, strategic_recommendation, "
            "risk, opportunity, key_insight, confidence (float)."
        )
        
        full_prompt = f"Company: {company}\nEvent Type: {event_type}\nHeadline: {title}\nDetails: {description}"

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=EventAnalysisResponse,
                    temperature=0.3,
                )
            )
            json_str = response.text
            if not json_str:
                raise RuntimeError("Empty response from Gemini")
            parsed = json.loads(json_str)
            return EventAnalysisResponse(**parsed)
        except Exception as e:
            logger.error(f"Gemini event analysis failed: {e}")
            raise RuntimeError(f"Gemini Event API failure: {e}")
