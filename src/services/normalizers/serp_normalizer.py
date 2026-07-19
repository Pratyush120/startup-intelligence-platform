from typing import List, Dict, Any
from src.models.intelligence import SearchResult, NewsArticle
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SerpNormalizer:
    @staticmethod
    def normalize_search(raw_results: List[Dict[str, Any]]) -> List[SearchResult]:
        normalized = []
        for item in raw_results:
            try:
                res = SearchResult(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    snippet=item.get("snippet", "")
                )
                normalized.append(res)
            except Exception as e:
                logger.debug(f"Failed to normalize search result: {e}")
        return normalized

    @staticmethod
    def normalize_news(raw_results: List[Dict[str, Any]]) -> List[NewsArticle]:
        normalized = []
        for item in raw_results:
            try:
                res = NewsArticle(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    publisher=item.get("source", "Web"),
                    published_at=item.get("date", ""),
                    snippet=item.get("snippet", "")
                )
                normalized.append(res)
            except Exception as e:
                logger.debug(f"Failed to normalize news result: {e}")
        return normalized
