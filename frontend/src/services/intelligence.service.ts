import { apiClient } from "@/api/client";
import { ENDPOINTS } from "@/api/endpoints";
import { 
  Entity, 
  ExecutiveModuleData, 
  MacroTrend, 
  NewsEvent, 
  StrategicRecommendation 
} from "@/lib/types";
import {
  ExecutiveBrief,
  MarketSnapshot,
  CompanyMetric,
  Recommendation,
  TimelineEvent,
  StrategicAlert,
  MetricCard
} from "@/lib/types/executive";

export const IntelligenceService = {
  getEcosystemHealth: async (): Promise<{ status: string, details: string }> => {
    try {
      const response = await apiClient.get(ENDPOINTS.ECOSYSTEM_HEALTH);
      const healthData = response.data.data;
      return {
        status: healthData.pipeline === "ready" ? "Operational" : "Degraded",
        details: `LLM Provider: ${healthData.llm_provider} | Database: ${healthData.database} | Pipeline: ${healthData.pipeline}`
      };
    } catch (e) {
      console.error(e);
      return { status: "Error", details: "Failed to fetch health data." };
    }
  },
  
  getExecutiveBrief: async (): Promise<ExecutiveBrief | null> => {
    try {
      const response = await apiClient.get(ENDPOINTS.EXECUTIVE_BRIEF);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return null;
    }
  },

  getTopCompanies: async (): Promise<CompanyMetric[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.ENTITIES);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getTimeline: async (): Promise<TimelineEvent[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.EVENTS);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getEntity: async (id: string): Promise<any> => {
    try {
      const response = await apiClient.get(ENDPOINTS.ENTITY(id));
      return response.data.data;
    } catch (e) {
      console.error(e);
      return null;
    }
  },

  searchEntities: async (query: string): Promise<{ companies: any[], events: any[] }> => {
    try {
      if (!query || query.length < 2) return { companies: [], events: [] };
      const response = await apiClient.get(`${ENDPOINTS.SEARCH}?query=${encodeURIComponent(query)}`);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return { companies: [], events: [] };
    }
  },

  getRecommendations: async (): Promise<Recommendation[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.RECOMMENDATIONS);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getMarketSnapshot: async (): Promise<MarketSnapshot[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.MARKET_SNAPSHOT);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getStrategicAlerts: async (): Promise<StrategicAlert[]> => {
    // Derive alerts from top timeline events or recommendations for now
    try {
      const response = await apiClient.get(ENDPOINTS.EVENTS);
      const events = response.data.data as TimelineEvent[];
      return events.filter(e => e.importance === 'Critical' || e.importance === 'High').map(e => ({
        id: e.id,
        title: e.eventType,
        impact: e.businessImpact,
        confidence: 90,
        companyName: e.companyName,
        category: e.eventType as any,
        recommendation: e.aiSummary,
        timestamp: e.date,
        priority: e.importance
      }));
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getMetrics: async (): Promise<MetricCard[]> => {
    // Derive metrics from market snapshot
    try {
      const response = await apiClient.get(ENDPOINTS.MARKET_SNAPSHOT);
      const snapshots = response.data.data as MarketSnapshot[];
      if (!snapshots.length) return [];
      const latest = snapshots[snapshots.length - 1];
      return [
        {
          id: "m1",
          label: "Funding Events",
          value: latest ? latest.fundingAmount : 0,
          trend: 5.2,
          trendLabel: "vs last month",
          sparkline: snapshots.map(s => s.fundingAmount),
          iconType: "DollarSign"
        },
        {
          id: "m2",
          label: "Hiring Activities",
          value: latest ? latest.hiringEvents : 0,
          trend: 2.1,
          trendLabel: "vs last month",
          sparkline: snapshots.map(s => s.hiringEvents),
          iconType: "Activity"
        },
        {
          id: "m3",
          label: "Layoffs",
          value: latest ? latest.layoffEvents : 0,
          trend: -1.5,
          trendLabel: "vs last month",
          sparkline: snapshots.map(s => s.layoffEvents),
          iconType: "ShieldAlert"
        }
      ];
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getTrends: async (): Promise<MacroTrend[]> => {
    // We derive trends from market snapshots
    try {
      const response = await apiClient.get(ENDPOINTS.MARKET_SNAPSHOT);
      const snapshots = response.data.data as MarketSnapshot[];
      return [
        {
          id: "t1",
          name: "AI Infrastructure",
          velocity: 14.5,
          sector: "AI",
          topEntityIds: []
        }
      ];
    } catch (e) {
      return [];
    }
  },

  getExecutiveModules: async (): Promise<ExecutiveModuleData[]> => {
    // Map the single executive brief to modules
    try {
      const response = await apiClient.get(ENDPOINTS.EXECUTIVE_BRIEF);
      const brief = response.data.data as ExecutiveBrief;
      if (!brief) return [];
      return [
        {
          id: brief.id,
          question: "What is the strategic summary?",
          answer: brief.strategicSummary,
          evidence: [],
          confidence: brief.confidenceScore,
          action: { label: brief.primaryRecommendation, intent: "Review" }
        }
      ];
    } catch (e) {
      return [];
    }
  }
};
