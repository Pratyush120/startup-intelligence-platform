import os
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SerpProvider:
    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")
        self.base_url = os.getenv("SERP_BASE_URL", "https://api.serper.dev")
        
        if not self.api_key:
            logger.warning("SERP_API_KEY is missing. SERP API will gracefully return empty/fallback data.")

    async def search_google(self, query: str) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
            
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
                    json={"q": query}
                )
                response.raise_for_status()
                data = response.json()
                return data.get("organic", [])
        except Exception as e:
            logger.error(f"SERP Search API failed for query '{query}': {e}")
            return []

    async def search_news(self, query: str) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
            
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{self.base_url}/news",
                    headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
                    json={"q": query}
                )
                response.raise_for_status()
                data = response.json()
                return data.get("news", [])
        except Exception as e:
            logger.error(f"SERP News API failed for query '{query}': {e}")
            return []
