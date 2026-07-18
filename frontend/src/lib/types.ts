export type Sentiment = 'positive' | 'negative' | 'neutral';
export type ThreatLevel = 'low' | 'moderate' | 'high' | 'critical';
export type EntityType = 'startup' | 'competitor' | 'enterprise' | 'investor';

export interface BusinessScore {
  overall: number; // 0-100
  momentum: number; // -100 to 100 (Velocity)
  financialHealth: number;
  marketPosition: number;
  threatLevel: ThreatLevel;
}

export interface NewsEvent {
  id: string;
  timestamp: string;
  source: string;
  headline: string;
  sentiment: Sentiment;
  impactScore: number; // 0-10
  vector: string; // The NLP categorized vector (e.g., 'Strategy Pivot', 'Executive Hire')
  summary: string;
}

export interface Entity {
  id: string;
  name: string;
  sector: string;
  type: EntityType;
  description: string;
  score: BusinessScore;
  recentEvents: NewsEvent[];
  competitors: string[]; // array of entity IDs
}

export interface StrategicRecommendation {
  id: string;
  title: string;
  description: string;
  targetEntityId: string | null;
  impact: string; // The "So What"
  probability: number; // 0-100
  generatedAt: string;
  mechanics: {
    dataPoints: number;
    primaryVector: string;
    confidence: number; // 0-100
  };
}

export interface MacroTrend {
  id: string;
  name: string;
  velocity: number; // Percentage growth in mentions/funding
  sector: string;
  topEntityIds: string[];
}

export interface ExecutiveModuleData {
  id: string;
  question: string;
  answer: string;
  evidence: {
    dataPoint: string;
    source: string;
  }[];
  confidence: number;
  action: {
    label: string;
    intent: string;
  };
}
