from typing import Dict, Any
from src.database.repository import Repository
from src.services.providers.serp_provider import SerpProvider
from src.services.normalizers.serp_normalizer import SerpNormalizer
from src.models.intelligence import CompanyIntelligence


class KnowledgeStore:
    def __init__(self, repo: Repository):
        self.repo = repo
        self.serp = SerpProvider()

    def get_company_intelligence(self, company_name: str) -> CompanyIntelligence:
        # Get from DB
        db_companies = self.repo.search_entities(company_name, limit=1)
        db_company = db_companies[0] if db_companies else {}

        description = db_company.get("sector", "Unknown Sector")

        # Get live news from SERP
        raw_news = self.serp.search_news(f"{company_name} startup funding OR news")
        recent_news = SerpNormalizer.normalize_news(raw_news)

        return CompanyIntelligence(
            company_name=company_name,
            description=description,
            recent_news=recent_news,
            related_searches=[],
        )

    def search_global(self, query: str) -> Dict[str, Any]:
        # Merge internal db and SERP
        db_companies = self.repo.search_entities(query, limit=5)
        db_events = self.repo.search_events(query, limit=5)

        # Fetch SERP data
        serp_news_raw = self.serp.search_news(query)
        serp_news = SerpNormalizer.normalize_news(serp_news_raw)

        return {
            "companies": db_companies,
            "events": db_events,
            "live_news": [n.model_dump() for n in serp_news],
        }
