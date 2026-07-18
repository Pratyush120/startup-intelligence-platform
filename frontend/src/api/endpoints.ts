export const ENDPOINTS = {
  ECOSYSTEM_HEALTH: "/health",
  MARKET_SNAPSHOT: "/market-snapshot",
  ENTITIES: "/companies",
  ENTITY: (id: string) => `/company/${id}`,
  EVENTS: "/timeline",
  RECOMMENDATIONS: "/recommendations",
  SEARCH: "/search",
  EXECUTIVE_BRIEF: "/executive-brief",
  PIPELINE_RUN: "/pipeline/run",
  PIPELINE_STATUS: "/pipeline/status",
} as const;
