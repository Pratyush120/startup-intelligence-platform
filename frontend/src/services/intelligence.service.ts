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
      const response = await apiClient.get(`${ENDPOINTS.SEARCH}?q=${encodeURIComponent(query)}`);
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
    try {
      const response = await apiClient.get(ENDPOINTS.STRATEGIC_ALERTS);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  runPipeline: async (): Promise<any> => {
    try {
      const response = await apiClient.post(ENDPOINTS.PIPELINE_RUN);
      return response.data;
    } catch (e) {
      console.error(e);
      throw e;
    }
  },

  getPipelineStatus: async (): Promise<any> => {
    try {
      const response = await apiClient.get(ENDPOINTS.PIPELINE_STATUS);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return null;
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
    try {
      const response = await apiClient.get(ENDPOINTS.TRENDS);
      return response.data.data;
    } catch (e) {
      return [];
    }
  },

  getExecutiveModules: async (): Promise<ExecutiveModuleData[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.EXECUTIVE_MODULES);
      return response.data.data;
    } catch (e) {
      return [];
    }
  },

  askCopilot: async (prompt: string): Promise<any> => {
    try {
      const response = await apiClient.post(ENDPOINTS.COPILOT_CHAT, { prompt });
      return response.data.data;
    } catch (e) {
      console.error(e);
      return {
        role: "assistant",
        content: "I encountered an error connecting to the intelligence backend."
      };
    }
  }
};
