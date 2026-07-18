import type { EventType, ImpactLevel } from "./common";

export interface IntelligenceEvent {
  id: string;
  entityId: string;
  entityName: string;
  eventType: EventType;
  headline: string;
  summary: string;
  impact: ImpactLevel;
  confidence: number;
  timestamp: string;
  source: string;
}
