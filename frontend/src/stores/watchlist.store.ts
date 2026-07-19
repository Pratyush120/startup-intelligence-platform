import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface WatchlistState {
  watchedEntityIds: string[];
  addEntity: (id: string) => void;
  removeEntity: (id: string) => void;
  isWatched: (id: string) => boolean;
}

export const useWatchlistStore = create<WatchlistState>()(
  persist(
    (set, get) => ({
      watchedEntityIds: [],
      
      addEntity: (id) => set((state) => ({
        watchedEntityIds: state.watchedEntityIds.includes(id) 
          ? state.watchedEntityIds 
          : [...state.watchedEntityIds, id]
      })),
      
      removeEntity: (id) => set((state) => ({
        watchedEntityIds: state.watchedEntityIds.filter(entityId => entityId !== id)
      })),
      
      isWatched: (id) => get().watchedEntityIds.includes(id),
    }),
    {
      name: 'sdip-watchlist-storage',
    }
  )
);
