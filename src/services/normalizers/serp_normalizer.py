from typing import List, Dict, Any
from datetime import datetime, timezone
from src.models.intelligence import NewsArticle, SourceAttribution
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SerpNormalizer:
    @staticmethod
    def normalize_news(raw_results: List[Dict[str, Any]]) -> List[NewsArticle]:
        normalized = []
        for item in raw_results:
            try:
                attribution = SourceAttribution(
                    provider="Google SERP",
                    url=item.get("link", ""),
                    retrieved_at=datetime.now(timezone.utc).isoformat(),
                    confidence=0.8,
                    provider_id="serper_news",
                )

                res = NewsArticle(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    publisher=item.get("source", "Web"),
                    published_at=item.get(
                        "date", datetime.now(timezone.utc).isoformat()
                    ),
                    snippet=item.get("snippet", ""),
                    source=attribution,
                )
                normalized.append(res)
            except Exception as e:
                logger.debug(f"Failed to normalize news result: {e}")
        return normalized
