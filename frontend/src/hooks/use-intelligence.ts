import { useQuery } from "@tanstack/react-query";
import { IntelligenceService } from "@/services/intelligence.service";

export function useEcosystemHealth() {
  return useQuery({
    queryKey: ["ecosystemHealth"],
    queryFn: IntelligenceService.getEcosystemHealth
  });
}

export function useExecutiveModules() {
  return useQuery({
    queryKey: ["executiveModules"],
    queryFn: IntelligenceService.getExecutiveModules
  });
}

export function useEntities() {
  return useQuery({
    queryKey: ["entities"],
    queryFn: IntelligenceService.getEntities
  });
}

export function useNewsEvents() {
  return useQuery({
    queryKey: ["newsEvents"],
    queryFn: IntelligenceService.getNewsEvents
  });
}
