import os
import httpx
from datetime import datetime, timezone
from typing import List
from src.utils.logger import get_logger
from src.models.intelligence import NewsArticle, SourceAttribution

logger = get_logger(__name__)


class NewsProvider:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        if not self.api_key:
            logger.warning(
                "NEWS_API_KEY is missing. NewsAPI provider will degrade gracefully."
            )
        self.base_url = "https://newsapi.org/v2"

    async def fetch_news(self, query: str) -> List[NewsArticle]:
        if not self.api_key:
            return []

        articles = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/everything",
                    params={
                        "q": query,
                        "apiKey": self.api_key,
                        "sortBy": "publishedAt",
                        "language": "en",
                        "pageSize": 5,
                    },
                )
                response.raise_for_status()
                data = response.json()

                for item in data.get("articles", []):
                    # Normalize directly to Intelligence Models
                    attribution = SourceAttribution(
                        provider="NewsAPI",
                        url=item.get("url"),
                        retrieved_at=datetime.now(timezone.utc).isoformat(),
                        confidence=0.9,
                        provider_id="newsapi_everything",
                    )

                    articles.append(
                        NewsArticle(
                            title=item.get("title", ""),
                            url=item.get("url", ""),
                            publisher=item.get("source", {}).get("name", "Unknown"),
                            published_at=item.get("publishedAt", ""),
                            snippet=item.get("description", "") or "",
                            source=attribution,
                        )
                    )
        except Exception as e:
            logger.error(f"NewsAPI request failed: {e}")

        return articles
