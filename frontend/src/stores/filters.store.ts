import { create } from "zustand";
import type { RiskLevel, SortField, SortOrder } from "@/types";

interface FiltersState {
  sector: string | null;
  riskLevel: RiskLevel | null;
  sortBy: SortField;
  sortOrder: SortOrder;
  setSector: (sector: string | null) => void;
  setRiskLevel: (level: RiskLevel | null) => void;
  setSortBy: (field: SortField) => void;
  toggleSortOrder: () => void;
  resetFilters: () => void;
}

const DEFAULTS = {
  sector: null,
  riskLevel: null,
  sortBy: "impact" as SortField,
  sortOrder: "desc" as SortOrder,
};

export const useFiltersStore = create<FiltersState>((set) => ({
  ...DEFAULTS,
  setSector: (sector) => set({ sector }),
  setRiskLevel: (level) => set({ riskLevel: level }),
  setSortBy: (field) => set({ sortBy: field }),
  toggleSortOrder: () => set((s) => ({ sortOrder: s.sortOrder === "asc" ? "desc" : "asc" })),
  resetFilters: () => set(DEFAULTS),
}));
