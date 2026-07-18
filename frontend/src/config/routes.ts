export const ROUTES = {
  HOME: "/",
  RADAR: "/radar",
  ENTITY: (id: string) => `/entities/${id}` as const,
  ENTITY_MECHANICS: (id: string) => `/entities/${id}?tab=mechanics` as const,
  STRATEGY: "/strategy",
  SCENARIO: (id: string) => `/strategy/scenarios/${id}` as const,
  TRENDS: (id: string) => `/trends/${id}` as const,
  REPORTS: "/reports",
  SETTINGS: "/settings",
  LOGIN: "/login",
} as const;
