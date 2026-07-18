import { Entity, MacroTrend, StrategicRecommendation, NewsEvent, ExecutiveModuleData } from './types';

export const mockEvents: NewsEvent[] = [
  {
    id: 'evt-1',
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 mins ago
    source: 'Bloomberg Terminal',
    headline: 'Nexus Robotics secures $120M Series C, pivots to autonomous warehouse logistics',
    sentiment: 'positive',
    impactScore: 8.5,
    vector: 'Funding & Pivot',
    summary: 'The latest funding round indicates a strong market shift towards fully autonomous fulfillment centers, moving away from human-assist models.'
  },
  {
    id: 'evt-2',
    timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(), // 2 hours ago
    source: 'Reuters',
    headline: 'Supply chain constraints ease in SE Asia, impacting localized manufacturing startups',
    sentiment: 'neutral',
    impactScore: 5.2,
    vector: 'Macro Economic Shift',
    summary: 'Easing of global shipping constraints reduces the immediate necessity for localized micro-manufacturing, potentially harming startups reliant on that thesis.'
  },
  {
    id: 'evt-3',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(),
    source: 'TechCrunch',
    headline: 'Former Stripe Executives launch stealth Fintech infrastructure play',
    sentiment: 'positive',
    impactScore: 7.1,
    vector: 'Executive Movement',
    summary: 'Top tier engineering talent migration detected. High probability of disruption in B2B payment orchestration.'
  },
  {
    id: 'evt-4',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    source: 'Financial Times',
    headline: 'European Union drafts new AI liability directive focusing on B2B SaaS',
    sentiment: 'negative',
    impactScore: 9.0,
    vector: 'Regulatory Action',
    summary: 'Pending legislation could increase compliance overhead by 40% for EU-based enterprise AI vendors.'
  }
];

export const mockEntities: Entity[] = [
  {
    id: 'ent-nexus',
    name: 'Nexus Robotics',
    sector: 'Supply Chain AI',
    type: 'startup',
    description: 'Autonomous warehouse logistics and fulfillment orchestration platform.',
    score: {
      overall: 88,
      momentum: 45,
      financialHealth: 92,
      marketPosition: 75,
      threatLevel: 'moderate'
    },
    recentEvents: [mockEvents[0]!],
    competitors: ['ent-auto-log']
  },
  {
    id: 'ent-stratos',
    name: 'Stratos Financial',
    sector: 'FinTech',
    type: 'competitor',
    description: 'Legacy payment gateway attempting transition to API-first infrastructure.',
    score: {
      overall: 64,
      momentum: -15,
      financialHealth: 70,
      marketPosition: 85,
      threatLevel: 'high'
    },
    recentEvents: [mockEvents[2]!], // threatened by the new startup
    competitors: []
  },
  {
    id: 'ent-aegis',
    name: 'Aegis AI',
    sector: 'Enterprise AI',
    type: 'startup',
    description: 'LLM-powered compliance and contract analysis.',
    score: {
      overall: 72,
      momentum: -5,
      financialHealth: 60,
      marketPosition: 40,
      threatLevel: 'critical'
    },
    recentEvents: [mockEvents[3]!], // Regulatory threat
    competitors: []
  }
];

export const mockRecommendations: StrategicRecommendation[] = [
  {
    id: 'rec-1',
    title: 'Monitor Nexus Robotics for potential acquisition',
    description: 'Following their Series C and pivot, Nexus poses a direct threat to our legacy fulfillment software suite. An acquisition before they dominate the mid-market is highly recommended.',
    targetEntityId: 'ent-nexus',
    impact: 'Preserves 15% market share in enterprise logistics software segment over the next 24 months.',
    probability: 85,
    generatedAt: new Date().toISOString(),
    mechanics: {
      dataPoints: 142,
      primaryVector: 'Funding & Pivot',
      confidence: 94
    }
  },
  {
    id: 'rec-2',
    title: 'Divest from EU-based Enterprise AI startups',
    description: 'Upcoming EU regulatory frameworks will disproportionately affect early-stage AI compliance startups, increasing burn rates.',
    targetEntityId: null,
    impact: 'Avoids projected 20% portfolio value degradation in the EU AI sector.',
    probability: 72,
    generatedAt: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    mechanics: {
      dataPoints: 56,
      primaryVector: 'Regulatory Action',
      confidence: 81
    }
  }
];

export const mockTrends: MacroTrend[] = [
  {
    id: 'trd-1',
    name: 'Autonomous Last-Mile',
    velocity: 125,
    sector: 'Supply Chain',
    topEntityIds: ['ent-nexus']
  },
  {
    id: 'trd-2',
    name: 'API-First B2B Payments',
    velocity: 84,
    sector: 'FinTech',
    topEntityIds: ['ent-stratos']
  },
  {
    id: 'trd-3',
    name: 'LLM Compliance Automation',
    velocity: -12,
    sector: 'Enterprise AI',
    topEntityIds: ['ent-aegis']
  }
];

export const mockExecutiveModules: ExecutiveModuleData[] = [
  {
    id: 'em-1',
    question: 'Is Nexus Robotics an immediate M&A target?',
    answer: 'Yes. Their recent pivot directly threatens our mid-market share in enterprise logistics. Acquiring them before Series D will neutralize the threat and absorb their proprietary autonomous stack.',
    evidence: [
      { dataPoint: '$120M Series C focused entirely on mid-market fulfillment.', source: 'Funding Event (Bloomberg)' },
      { dataPoint: '3 key engineering hires from our logistics division.', source: 'Executive Movement (LinkedIn)' }
    ],
    confidence: 94,
    action: {
      label: 'Draft Acquisition Memo',
      intent: 'initiate-ma'
    }
  },
  {
    id: 'em-2',
    question: 'Should we divest from EU-based Enterprise AI startups?',
    answer: 'We recommend pausing further investment until Q4. Impending regulatory frameworks will disproportionately increase compliance overhead and burn rates for early-stage AI vendors in this jurisdiction.',
    evidence: [
      { dataPoint: 'Draft EU AI liability directive mandates extensive compliance auditing.', source: 'Regulatory Action (Financial Times)' },
      { dataPoint: 'Average burn rate for EU AI startups increased by 18% last quarter.', source: 'Market Intelligence' }
    ],
    confidence: 82,
    action: {
      label: 'Pause Capital Deployment',
      intent: 'update-strategy'
    }
  }
];
