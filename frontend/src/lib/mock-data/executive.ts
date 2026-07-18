import {
  ExecutiveBrief,
  StrategicAlert,
  MarketSnapshot,
  CompanyMetric,
  Recommendation,
  TimelineEvent,
  MetricCard
} from '../types/executive';

export const mockExecutiveBrief: ExecutiveBrief = {
  id: 'eb_101',
  date: new Date().toISOString(),
  marketHealthScore: 82,
  investmentClimate: 'Favorable',
  riskLevel: 'Medium',
  growthOutlook: 'Accelerating',
  strategicSummary: 'AI infrastructure startups continue to dominate funding while fintech investment slows. Market concentration in generative AI models is reaching critical density.',
  confidenceScore: 94,
  primaryRecommendation: 'Consider monitoring enterprise AI vendors over the next 30 days. High probability of M&A activity in the vector database sector.'
};

export const mockStrategicAlerts: StrategicAlert[] = [
  {
    id: 'sa_1',
    title: 'OpenAI acquires Rockset',
    impact: 'Massive consolidation in real-time analytics space.',
    confidence: 99,
    companyName: 'OpenAI',
    category: 'Acquisition',
    recommendation: 'Review portfolio exposure to standalone vector databases.',
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    priority: 'Critical'
  },
  {
    id: 'sa_2',
    title: 'Anthropic raises $2.7B Series D',
    impact: 'Increases valuation pressure on smaller foundation model companies.',
    confidence: 95,
    companyName: 'Anthropic',
    category: 'Funding',
    recommendation: 'Hold early-stage investments in foundation models.',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
    priority: 'High'
  },
  {
    id: 'sa_3',
    title: 'Stripe reinstates crypto payments',
    impact: 'Signals regulatory thawing in US crypto markets.',
    confidence: 88,
    companyName: 'Stripe',
    category: 'Market Shift',
    recommendation: 'Evaluate stalled crypto infrastructure deals.',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    priority: 'Medium'
  }
];

export const mockMetrics: MetricCard[] = [
  {
    id: 'm_1',
    label: 'Companies Tracked',
    value: '14,208',
    trend: 1.2,
    trendLabel: 'vs last week',
    sparkline: [12000, 12500, 13100, 13800, 14208],
    iconType: 'Building'
  },
  {
    id: 'm_2',
    label: 'Funding Tracked Today',
    value: '$3.4B',
    trend: 45.2,
    trendLabel: 'vs 30d avg',
    sparkline: [1.2, 0.8, 1.5, 0.9, 3.4],
    iconType: 'DollarSign'
  },
  {
    id: 'm_3',
    label: 'Avg Momentum Score',
    value: 78,
    trend: -2.1,
    trendLabel: 'vs last week',
    sparkline: [82, 85, 80, 81, 78],
    iconType: 'Activity'
  },
  {
    id: 'm_4',
    label: 'Intelligence Confidence',
    value: '94%',
    trend: 0.5,
    trendLabel: 'vs yesterday',
    sparkline: [92, 91, 93, 93, 94],
    iconType: 'BrainCircuit'
  }
];

export const mockMarketSnapshots: MarketSnapshot[] = Array.from({ length: 30 }).map((_, i) => ({
  date: new Date(Date.now() - 1000 * 60 * 60 * 24 * (30 - i)).toISOString().split('T')[0] || "",
  fundingAmount: Math.floor(Math.random() * 500) + 100,
  hiringEvents: Math.floor(Math.random() * 200) + 50,
  layoffEvents: Math.floor(Math.random() * 50) + 5,
}));

export const mockTopCompanies: CompanyMetric[] = [
  {
    id: 'c_1',
    name: 'OpenAI',
    momentum: 98,
    fundingTotal: 13000000000,
    growthScore: 95,
    riskScore: 20,
    recommendation: 'Strong Hold',
    trendDirection: 'up',
    sparklineData: [80, 85, 90, 95, 98]
  },
  {
    id: 'c_2',
    name: 'Anthropic',
    momentum: 95,
    fundingTotal: 7300000000,
    growthScore: 92,
    riskScore: 25,
    recommendation: 'Buy',
    trendDirection: 'up',
    sparklineData: [75, 80, 85, 92, 95]
  },
  {
    id: 'c_3',
    name: 'Mistral AI',
    momentum: 88,
    fundingTotal: 650000000,
    growthScore: 89,
    riskScore: 40,
    recommendation: 'Monitor',
    trendDirection: 'flat',
    sparklineData: [85, 88, 86, 89, 88]
  }
];

export const mockRecommendations: Recommendation[] = [
  {
    id: 'r_1',
    title: 'Increase Exposure to Enterprise AI Agents',
    reason: 'Funding velocity in agentic workflows has increased 300% Q/Q.',
    evidence: [
      'Devin (Cognition) raised at $2B valuation.',
      'AutoGPT enterprise usage up 45%.',
      'Microsoft Copilot adoption exceeds expectations.'
    ],
    confidence: 88,
    suggestedAction: 'Review top 10 fastest growing agent startups for potential investment.',
    priority: 'High',
    strategicImpact: 'Critical positioning for the next phase of LLM commercialization.',
    estimatedOpportunity: '$50M - $150M TAM Expansion',
    estimatedRisk: 'High execution risk; market is extremely crowded.',
    timestamp: new Date().toISOString(),
    evidenceScore: 92,
    relatedCompanies: ['Cognition', 'Microsoft', 'LangChain'],
    relatedEvents: ['te_1', 'te_2']
  }
];

export const mockTimelineEvents: TimelineEvent[] = [
  {
    id: 'te_1',
    companyName: 'Vercel',
    eventType: 'Product Launch',
    date: new Date().toISOString(),
    importance: 'Medium',
    businessImpact: 'Strengthens enterprise serverless offering.',
    aiSummary: 'Vercel launched v0, integrating generative UI into their developer platform.'
  },
  {
    id: 'te_2',
    companyName: 'Stripe',
    eventType: 'Acquisition',
    date: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(), // 12 hours ago
    importance: 'High',
    businessImpact: 'Consolidates crypto-to-fiat onramps.',
    aiSummary: 'Stripe acquired Bridge to bolster their stablecoin infrastructure.'
  },
  {
    id: 'te_3',
    companyName: 'OpenAI',
    eventType: 'Funding',
    date: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(), // 2 days ago
    importance: 'Critical',
    businessImpact: 'Sets new valuation benchmark for foundation models.',
    aiSummary: 'OpenAI raised a monumental round at a $150B valuation.'
  },
  {
    id: 'te_4',
    companyName: 'Stability AI',
    eventType: 'Layoff',
    date: new Date(Date.now() - 1000 * 60 * 60 * 24 * 7).toISOString(), // 7 days ago
    importance: 'Medium',
    businessImpact: 'Signals stress in open-source AI business models.',
    aiSummary: 'Stability AI announced a 10% reduction in workforce citing restructuring.'
  }
];
