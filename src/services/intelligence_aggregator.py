import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import hashlib

from src.database.repository import Repository
from src.services.providers.serp_provider import SerpProvider
from src.services.providers.news_provider import NewsProvider
from src.services.providers.finnhub_provider import FinnhubProvider
from src.services.normalizers.serp_normalizer import SerpNormalizer
from src.models.intelligence import CompanyProfile, NewsArticle, TimelineEvent, FinancialMetric
from src.utils.cache import global_cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

class IntelligenceAggregator:
    def __init__(self, repo: Repository):
        self.repo = repo
        self.serp = SerpProvider()
        self.news = NewsProvider()
        self.finnhub = FinnhubProvider()

    async def _fetch_serp(self, query: str) -> List[NewsArticle]:
        cache_key = f"serp:news:{query}"
        cached = global_cache.get(cache_key)
        if cached:
            return cached
            
        raw = await self.serp.search_news(f"{query} startup OR company")
        normalized = SerpNormalizer.normalize_news(raw)
        global_cache.set(cache_key, normalized, ttl_seconds=1800) # 30 min
        return normalized

    async def _fetch_newsapi(self, query: str) -> List[NewsArticle]:
        cache_key = f"newsapi:{query}"
        cached = global_cache.get(cache_key)
        if cached:
            return cached
            
        articles = await self.news.fetch_news(query)
        global_cache.set(cache_key, articles, ttl_seconds=900) # 15 min
        return articles

    async def _fetch_finnhub(self, query: str) -> List[FinancialMetric]:
        cache_key = f"finnhub:{query}"
        cached = global_cache.get(cache_key)
        if cached:
            return cached
            
        financials = await self.finnhub.fetch_financials(query)
        global_cache.set(cache_key, financials, ttl_seconds=1800) # 30 min
        return financials

    def _fetch_db_company(self, query: str) -> Dict[str, Any]:
        companies = self.repo.search_entities(query, limit=1)
        return companies[0] if companies else {}

    def _fetch_db_events(self, query: str) -> List[Dict[str, Any]]:
        return self.repo.search_events(query, limit=10)

    def _deduplicate_news(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        seen_urls = set()
        seen_titles = set()
        unique = []
        for a in articles:
            url_hash = hashlib.md5(a.url.encode()).hexdigest()
            title_hash = hashlib.md5(a.title.lower().strip().encode()).hexdigest()
            if url_hash not in seen_urls and title_hash not in seen_titles:
                seen_urls.add(url_hash)
                seen_titles.add(title_hash)
                unique.append(a)
        return unique

    def _rank_news(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        # Rank by freshness and provider trust
        def get_score(a: NewsArticle) -> float:
            score = 0.0
            if a.source.provider == "Finnhub":
                score += 1.0
            elif a.source.provider == "NewsAPI":
                score += 0.8
            else:
                score += 0.5
            return score
            
        # Basic sort by score (descending)
        return sorted(articles, key=get_score, reverse=True)

    async def build_company_intelligence(self, company_name: str) -> CompanyProfile:
        # CONCURRENT AGGREGATION
        results = await asyncio.gather(
            asyncio.to_thread(self._fetch_db_company, company_name),
            self._fetch_serp(company_name),
            self._fetch_newsapi(company_name),
            self._fetch_finnhub(company_name),
            return_exceptions=True
        )

        db_company, serp_news, newsapi_articles, financials = results

        # Handle exceptions gracefully
        if isinstance(db_company, Exception):
            db_company = {}
        if isinstance(serp_news, Exception):
            serp_news = []
        if isinstance(newsapi_articles, Exception):
            newsapi_articles = []
        if isinstance(financials, Exception):
            financials = []

        all_news = serp_news + newsapi_articles
        unique_news = self._deduplicate_news(all_news)
        ranked_news = self._rank_news(unique_news)

        from src.models.intelligence import SourceAttribution
        
        return CompanyProfile(
            company_name=db_company.get("company_name", company_name),
            website=db_company.get("website"),
            description=db_company.get("sector", "Technology"),
            financials=financials,
            source=SourceAttribution(
                provider="Aggregator",
                retrieved_at=datetime.now(timezone.utc).isoformat(),
                confidence=0.95
            ),
            # Keep top 10 news for context
            competitors=[] 
        )
        
    async def build_global_context(self, query: str) -> Dict[str, Any]:
        # Fetch everything concurrently
        results = await asyncio.gather(
            asyncio.to_thread(self._fetch_db_company, query),
            asyncio.to_thread(self._fetch_db_events, query),
            self._fetch_serp(query),
            self._fetch_newsapi(query),
            self._fetch_finnhub(query),
            return_exceptions=True
        )
        
        db_company, db_events, serp_news, newsapi_articles, financials = results
        
        if isinstance(db_company, Exception): db_company = {}
        if isinstance(db_events, Exception): db_events = []
        if isinstance(serp_news, Exception): serp_news = []
        if isinstance(newsapi_articles, Exception): newsapi_articles = []
        if isinstance(financials, Exception): financials = []

        all_news = self._rank_news(self._deduplicate_news(serp_news + newsapi_articles))
        
        return {
            "company": db_company.get("company_name", query),
            "business_summary": db_company.get("sector", ""),
            "financials": financials,
            "latest_news": all_news[:5],
            "db_events": db_events
        }
