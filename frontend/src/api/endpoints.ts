export const ENDPOINTS = {
  ECOSYSTEM_HEALTH: "/ecosystem/health",
  STRATEGIC_CHANGES: "/ecosystem/changes",
  MARKET_SNAPSHOT: "/market/snapshot",
  ENTITIES: "/entities",
  ENTITY: (id: string) => `/entities/${id}`,
  ENTITY_MECHANICS: (id: string) => `/entities/${id}/mechanics`,
  EVENTS: "/events",
  RECOMMENDATIONS: "/recommendations",
  TRENDS: "/trends",
  TREND: (id: string) => `/trends/${id}`,
  SCENARIOS: "/scenarios",
  SCENARIO: (id: string) => `/scenarios/${id}`,
} as const;
