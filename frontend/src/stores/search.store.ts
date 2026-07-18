import { create } from "zustand";
import { persist } from "zustand/middleware";
import { MAX_RECENT_SEARCHES } from "@/config/constants";

interface SearchState {
  recentSearches: string[];
  addRecentSearch: (query: string) => void;
  clearRecentSearches: () => void;
}

export const useSearchStore = create<SearchState>()(
  persist(
    (set) => ({
      recentSearches: [],

      addRecentSearch: (query) =>
        set((s) => ({
          recentSearches: [
            query,
            ...s.recentSearches.filter((q) => q !== query),
          ].slice(0, MAX_RECENT_SEARCHES),
        })),

      clearRecentSearches: () => set({ recentSearches: [] }),
    }),
    { name: "sdip-search" }
  )
);
