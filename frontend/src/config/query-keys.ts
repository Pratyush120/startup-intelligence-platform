export const queryKeys = {
  ecosystem: {
    health: () => ["ecosystem", "health"] as const,
    changes: () => ["ecosystem", "changes"] as const,
    snapshot: () => ["ecosystem", "snapshot"] as const,
  },
  entities: {
    all: () => ["entities"] as const,
    list: (filters?: Record<string, unknown>) => ["entities", "list", filters] as const,
    detail: (id: string) => ["entities", "detail", id] as const,
    mechanics: (id: string) => ["entities", "detail", id, "mechanics"] as const,
  },
  events: {
    all: () => ["events"] as const,
    list: (filters?: Record<string, unknown>) => ["events", "list", filters] as const,
  },
  recommendations: {
    list: () => ["recommendations", "list"] as const,
  },
  trends: {
    all: () => ["trends"] as const,
    list: () => ["trends", "list"] as const,
    detail: (id: string) => ["trends", "detail", id] as const,
  },
  scenarios: {
    all: () => ["scenarios"] as const,
    list: () => ["scenarios", "list"] as const,
    detail: (id: string) => ["scenarios", "detail", id] as const,
  },
} as const;
