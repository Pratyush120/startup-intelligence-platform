export interface ExecutiveBrief {
  id: string;
  date: string;
  marketHealthScore: number;
  investmentClimate: 'Favorable' | 'Neutral' | 'Hostile';
  riskLevel: 'Critical' | 'High' | 'Medium' | 'Low';
  growthOutlook: 'Accelerating' | 'Stable' | 'Decelerating';
  strategicSummary: string;
  confidenceScore: number;
  primaryRecommendation: string;
}

export interface StrategicAlert {
  id: string;
  title: string;
  impact: string;
  confidence: number;
  companyId?: string;
  companyName?: string;
  category: 'Funding' | 'Acquisition' | 'Leadership' | 'Layoff' | 'Expansion' | 'Market Shift';
  recommendation: string;
  timestamp: string;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
}

export interface MarketSnapshot {
  date: string;
  fundingAmount: number;
  hiringEvents: number;
  layoffEvents: number;
}

export interface CompanyMetric {
  id: string;
  name: string;
  momentum: number;
  fundingTotal: number;
  growthScore: number;
  riskScore: number;
  recommendation: string;
  trendDirection: 'up' | 'down' | 'flat';
  sparklineData: number[];
}

export interface Recommendation {
  id: string;
  title: string;
  reason: string;
  evidence: string[];
  confidence: number;
  suggestedAction: string;
  priority: 'High' | 'Medium' | 'Low';
  strategicImpact: string;
  estimatedOpportunity: string;
  estimatedRisk: string;
  timestamp: string;
  evidenceScore: number;
  relatedCompanies: string[];
  relatedEvents: string[];
}

export interface TimelineEvent {
  id: string;
  companyName: string;
  eventType: string;
  date: string;
  importance: 'Critical' | 'High' | 'Medium' | 'Low';
  businessImpact: string;
  aiSummary: string;
}

export interface MetricCard {
  id: string;
  label: string;
  value: string | number;
  trend: number; // e.g. 2.4 for +2.4%
  trendLabel: string;
  sparkline: number[];
  iconType: 'Building' | 'DollarSign' | 'Activity' | 'TrendingUp' | 'ShieldAlert' | 'BrainCircuit';
}
