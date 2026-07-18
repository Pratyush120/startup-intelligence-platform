import { mockEntities, mockEvents, mockExecutiveModules, mockRecommendations, mockTrends } from "@/lib/mockData";
import { Entity, ExecutiveModuleData, MacroTrend, NewsEvent, StrategicRecommendation } from "@/lib/types";

// In Milestone 7, these will be replaced with actual apiClient calls
// e.g. return (await apiClient.get<Entity[]>("/entities")).data;

export const IntelligenceService = {
  getEcosystemHealth: async (): Promise<{ status: string, details: string }> => {
    return new Promise((resolve) => setTimeout(() => resolve({
      status: "Elevated Velocity",
      details: "Capital deployment has surged 14% week-over-week..."
    }), 300));
  },
  
  getExecutiveModules: async (): Promise<ExecutiveModuleData[]> => {
    return new Promise((resolve) => setTimeout(() => resolve(mockExecutiveModules), 400));
  },

  getEntities: async (): Promise<Entity[]> => {
    return new Promise((resolve) => setTimeout(() => resolve(mockEntities), 350));
  },

  getNewsEvents: async (): Promise<NewsEvent[]> => {
    return new Promise((resolve) => setTimeout(() => resolve(mockEvents), 250));
  },

  getTrends: async (): Promise<MacroTrend[]> => {
    return new Promise((resolve) => setTimeout(() => resolve(mockTrends), 300));
  },

  getRecommendations: async (): Promise<StrategicRecommendation[]> => {
    return new Promise((resolve) => setTimeout(() => resolve(mockRecommendations), 500));
  }
};
