import { create } from "zustand";

interface UIState {
  sidebarCollapsed: boolean;
  overlayStack: string[];
  commandPaletteOpen: boolean;
  explainabilityDrawer: {
    open: boolean;
    moduleId: string | null;
    moduleName: string | null;
  };

  toggleSidebar: () => void;
  openCommandPalette: () => void;
  closeCommandPalette: () => void;
  openExplainability: (moduleId: string, moduleName: string) => void;
  closeExplainability: () => void;
  closeTopOverlay: () => void;
}

export const useUIStore = create<UIState>((set, get) => ({
  sidebarCollapsed: false,
  overlayStack: [],
  commandPaletteOpen: false,
  explainabilityDrawer: { open: false, moduleId: null, moduleName: null },

  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),

  openCommandPalette: () =>
    set((s) => ({
      commandPaletteOpen: true,
      overlayStack: [...s.overlayStack, "command-palette"],
    })),

  closeCommandPalette: () =>
    set((s) => ({
      commandPaletteOpen: false,
      overlayStack: s.overlayStack.filter((o) => o !== "command-palette"),
    })),

  openExplainability: (moduleId, moduleName) =>
    set((s) => ({
      explainabilityDrawer: { open: true, moduleId, moduleName },
      overlayStack: [...s.overlayStack, "explainability"],
    })),

  closeExplainability: () =>
    set((s) => ({
      explainabilityDrawer: { open: false, moduleId: null, moduleName: null },
      overlayStack: s.overlayStack.filter((o) => o !== "explainability"),
    })),

  closeTopOverlay: () => {
    const stack = get().overlayStack;
    const top = stack[stack.length - 1];
    if (top === "command-palette") get().closeCommandPalette();
    else if (top === "explainability") get().closeExplainability();
  },
}));
