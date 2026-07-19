from pydantic import BaseModel, Field
from typing import List, Optional

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    source: str = "google"

class NewsArticle(BaseModel):
    title: str
    url: str
    publisher: str
    published_at: str
    snippet: str

class TrendPoint(BaseModel):
    keyword: str
    momentum: float
    timeframe: str = "7d"

class MarketSignal(BaseModel):
    signal_type: str
    description: str
    impact_score: float
    
class CompanyIntelligence(BaseModel):
    company_name: str
    website: Optional[str] = None
    description: str
    recent_news: List[NewsArticle] = Field(default_factory=list)
    related_searches: List[str] = Field(default_factory=list)

class CopilotResponse(BaseModel):
    summary: str
    key_insights: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    competitor_perspective: str = ""
    confidence: float
    sources: List[str] = Field(default_factory=list)
