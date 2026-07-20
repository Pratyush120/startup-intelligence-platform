from pydantic import BaseModel, Field
from typing import List, Optional


class SourceAttribution(BaseModel):
    provider: str
    url: Optional[str] = None
    retrieved_at: str
    confidence: float
    provider_id: Optional[str] = None


class NewsArticle(BaseModel):
    title: str
    url: str
    publisher: str
    published_at: str
    snippet: str
    source: SourceAttribution


class TimelineEvent(BaseModel):
    title: str
    event_type: str
    date: str
    description: str
    source: SourceAttribution


class Trend(BaseModel):
    keyword: str
    momentum: float
    timeframe: str = "7d"
    source: SourceAttribution


class MarketSignal(BaseModel):
    signal_type: str
    description: str
    impact_score: float
    source: SourceAttribution


class FinancialMetric(BaseModel):
    metric_name: str
    value: float
    currency: Optional[str] = "USD"
    source: SourceAttribution


class Competitor(BaseModel):
    name: str
    similarity_score: float
    source: SourceAttribution


class CompanyProfile(BaseModel):
    company_name: str
    website: Optional[str] = None
    description: str
    industry: Optional[str] = None
    financials: List[FinancialMetric] = Field(default_factory=list)
    competitors: List[Competitor] = Field(default_factory=list)
    source: SourceAttribution


class Recommendation(BaseModel):
    action: str
    reasoning: str
    impact: str


class ExecutiveBrief(BaseModel):
    summary: str
    market_health: float
    risk_level: str
    growth_outlook: str
    signals: List[MarketSignal] = Field(default_factory=list)
    trends: List[Trend] = Field(default_factory=list)


class CopilotResponse(BaseModel):
    summary: str
    key_insights: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    competitor_perspective: str = ""
    confidence: float
    sources: List[str] = Field(default_factory=list)


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
