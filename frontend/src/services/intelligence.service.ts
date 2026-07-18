import { apiClient } from "@/api/client";
import { ENDPOINTS } from "@/api/endpoints";
import { Entity, ExecutiveModuleData, MacroTrend, NewsEvent, StrategicRecommendation } from "@/lib/types";
import { mockTrends, mockExecutiveModules } from "@/lib/mockData"; // Keep for remaining mock components

export const IntelligenceService = {
  getEcosystemHealth: async (): Promise<{ status: string, details: string }> => {
    try {
      const response = await apiClient.get(ENDPOINTS.ECOSYSTEM_HEALTH);
      // Map API response to expected UI format
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
  
  getExecutiveModules: async (): Promise<ExecutiveModuleData[]> => {
    // For this milestone, we use the mock executive modules because the backend returns 
    // a single ExecutiveBrief object whereas the frontend uses ExecutiveModuleData[].
    // Wait, the UI uses ExecutiveBrief in some places and ExecutiveModuleData in others?
    // Let's preserve the mock here for the specific useExecutiveModules hook, since 
    // the backend doesn't return ExecutiveModuleData array.
    return new Promise((resolve) => setTimeout(() => resolve(mockExecutiveModules), 400));
  },

  getEntities: async (): Promise<Entity[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.ENTITIES);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getNewsEvents: async (): Promise<NewsEvent[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.EVENTS);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getTrends: async (): Promise<MacroTrend[]> => {
    // Trends is not implemented in FastAPI yet, keep mock
    return new Promise((resolve) => setTimeout(() => resolve(mockTrends), 300));
  },

  getRecommendations: async (): Promise<StrategicRecommendation[]> => {
    try {
      const response = await apiClient.get(ENDPOINTS.RECOMMENDATIONS);
      return response.data.data;
    } catch (e) {
      console.error(e);
      return [];
    }
  }
};
