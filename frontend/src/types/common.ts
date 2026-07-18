export type RiskLevel = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";

export type EcosystemStatus = "ELEVATED_VELOCITY" | "STABLE" | "RISK_CONDITIONS_PRESENT";

export type EventType = "FUNDING" | "ACQUISITION" | "LEADERSHIP_CHANGE" | "REGULATORY" | "MARKET_ENTRY" | "PARTNERSHIP";

export type ImpactLevel = "HIGH" | "MEDIUM" | "LOW";

export type Sentiment = "POSITIVE" | "NEUTRAL" | "NEGATIVE";

export type SortOrder = "asc" | "desc";

export type SortField = "impact" | "recency" | "score";

export interface Pagination {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}

export interface ApiError {
  status: number;
  message: string;
  code?: string;
}
