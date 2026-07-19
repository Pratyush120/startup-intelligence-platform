import { create } from 'zustand';

interface UIState {
  isCopilotOpen: boolean;
  toggleCopilot: () => void;
  openCopilot: () => void;
  closeCopilot: () => void;
  
  isSearchOpen: boolean;
  toggleSearch: () => void;
  openSearch: () => void;
  closeSearch: () => void;

  isCompareOpen: boolean;
  toggleCompare: () => void;
  openCompare: () => void;
  closeCompare: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  isCopilotOpen: false,
  toggleCopilot: () => set((state) => ({ isCopilotOpen: !state.isCopilotOpen })),
  openCopilot: () => set({ isCopilotOpen: true }),
  closeCopilot: () => set({ isCopilotOpen: false }),

  isSearchOpen: false,
  toggleSearch: () => set((state) => ({ isSearchOpen: !state.isSearchOpen })),
  openSearch: () => set({ isSearchOpen: true }),
  closeSearch: () => set({ isSearchOpen: false }),

  isCompareOpen: false,
  toggleCompare: () => set((state) => ({ isCompareOpen: !state.isCompareOpen })),
  openCompare: () => set({ isCompareOpen: true }),
  closeCompare: () => set({ isCompareOpen: false }),
}));
