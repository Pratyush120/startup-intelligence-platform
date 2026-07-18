import type { RiskLevel } from "./common";

export interface Entity {
  id: string;
  name: string;
  sector: string;
  description: string;
  healthScore: number;
  healthDelta: number;
  growthData: number[];
  riskLevel: RiskLevel;
  signal: string;
  competitors: string[];
  founded: string;
  headquarters: string;
  employeeCount: number;
  totalFunding: number;
  lastFundingRound: string;
  lastFundingAmount: number;
}
