import { useQuery } from "@tanstack/react-query";
import { IntelligenceService } from "@/services/intelligence.service";

// Set a standard stale time of 1 minute to prevent spamming the backend
const STALE_TIME = 60 * 1000;

export function useEcosystemHealth() {
  return useQuery({
    queryKey: ["ecosystemHealth"],
    queryFn: IntelligenceService.getEcosystemHealth,
    staleTime: STALE_TIME,
  });
}

export function useExecutiveBrief() {
  return useQuery({
    queryKey: ["executiveBrief"],
    queryFn: IntelligenceService.getExecutiveBrief,
    staleTime: STALE_TIME,
  });
}

export function useTopCompanies() {
  return useQuery({
    queryKey: ["topCompanies"],
    queryFn: IntelligenceService.getTopCompanies,
    staleTime: STALE_TIME,
  });
}

export function useEntity(id: string) {
  return useQuery({
    queryKey: ["entity", id],
    queryFn: () => IntelligenceService.getEntity(id),
    staleTime: STALE_TIME,
    enabled: !!id,
  });
}

export function useSearch(query: string) {
  return useQuery({
    queryKey: ["search", query],
    queryFn: () => IntelligenceService.searchEntities(query),
    staleTime: STALE_TIME,
    enabled: query.length >= 2,
  });
}

export function useTimeline() {
  return useQuery({
    queryKey: ["timeline"],
    queryFn: IntelligenceService.getTimeline,
    staleTime: STALE_TIME,
  });
}

export function useRecommendations() {
  return useQuery({
    queryKey: ["recommendations"],
    queryFn: IntelligenceService.getRecommendations,
    staleTime: STALE_TIME,
  });
}

export function useMarketSnapshot() {
  return useQuery({
    queryKey: ["marketSnapshot"],
    queryFn: IntelligenceService.getMarketSnapshot,
    staleTime: STALE_TIME,
  });
}

export function useStrategicAlerts() {
  return useQuery({
    queryKey: ["strategicAlerts"],
    queryFn: IntelligenceService.getStrategicAlerts,
    staleTime: STALE_TIME,
  });
}

export function useMetrics() {
  return useQuery({
    queryKey: ["metrics"],
    queryFn: IntelligenceService.getMetrics,
    staleTime: STALE_TIME,
  });
}

export function useTrends() {
  return useQuery({
    queryKey: ["trends"],
    queryFn: IntelligenceService.getTrends,
    staleTime: STALE_TIME,
  });
}

export function useExecutiveModules() {
  return useQuery({
    queryKey: ["executiveModules"],
    queryFn: IntelligenceService.getExecutiveModules,
    staleTime: STALE_TIME,
  });
}

export function usePipelineStatus() {
  return useQuery({
    queryKey: ["pipelineStatus"],
    queryFn: IntelligenceService.getPipelineStatus,
    staleTime: 0, // Always fetch latest status
    refetchInterval: 5000, // Poll every 5s if active, could be dynamic
  });
}

import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useRunPipeline() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: IntelligenceService.runPipeline,
    onSuccess: () => {
      // Invalidate queries to refresh data across the app
      queryClient.invalidateQueries({ queryKey: ["pipelineStatus"] });
      queryClient.invalidateQueries({ queryKey: ["executiveBrief"] });
      queryClient.invalidateQueries({ queryKey: ["topCompanies"] });
      queryClient.invalidateQueries({ queryKey: ["timeline"] });
    },
  });
}
