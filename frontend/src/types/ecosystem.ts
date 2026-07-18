import type { EcosystemStatus } from "./common";

export interface EcosystemHealth {
  status: EcosystemStatus;
  sentiment: string;
  summary: string;
  signalsProcessed: number;
  lastUpdated: string;
  capitalDelta: number;
}

export interface StrategicChange {
  id: string;
  entityId: string;
  entityName: string;
  changeType: string;
  summary: string;
  impact: string;
  timestamp: string;
}

export interface MarketSnapshot {
  fundingDistribution: { category: string; value: number }[];
  hiringActivity: number[];
  riskDistribution: { level: string; percentage: number }[];
}
