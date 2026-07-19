"use client";

import { useState } from "react";
import { Building2, Plus, Sparkles, AlertCircle, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { useUIStore } from "@/store/ui.store";

export default function WatchlistPage() {
  const [watchlist, setWatchlist] = useState<any[]>([]);
  const router = useRouter();
  const openSearch = useUIStore(state => state.openSearch);

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8 h-full flex flex-col">
      <div className="flex items-center justify-between border-b border-border-default pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-primary">My Watchlist</h1>
          <p className="text-sm text-secondary mt-1">Monitor strategic entities and market competitors.</p>
        </div>
        <button 
          onClick={openSearch}
          className="px-4 py-2 bg-primary text-primary-foreground hover:bg-primary/90 rounded-md text-sm font-medium transition-colors flex items-center gap-2 shadow-sm"
        >
          <Plus className="w-4 h-4" />
          Add Entity
        </button>
      </div>

      {watchlist.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-border-default rounded-xl bg-surface-1 p-12 text-center animate-in fade-in duration-500">
          <div className="w-16 h-16 bg-surface-2 rounded-2xl flex items-center justify-center text-secondary mb-6">
            <Building2 className="w-8 h-8" />
          </div>
          <h2 className="text-xl font-bold text-primary">Your Watchlist is Empty</h2>
          <p className="text-secondary mt-2 max-w-md mx-auto leading-relaxed">
            Start tracking companies, competitors, and market trends to generate automated strategic insights.
          </p>
          
          <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-2xl">
            <button 
              onClick={() => router.push('/entities/demo')}
              className="p-5 rounded-xl border border-border-default hover:border-border-strong bg-surface-2 hover:bg-surface-3 transition-colors text-left flex items-start gap-4 group"
            >
               <Sparkles className="w-5 h-5 text-signal-positive shrink-0" />
               <div>
                  <h3 className="font-medium text-primary group-hover:text-primary transition-colors">Add Market Leader</h3>
                  <p className="text-xs text-secondary mt-1">Track high-momentum companies like OpenAI or Anthropic.</p>
               </div>
            </button>
            <button 
              onClick={openSearch}
              className="p-5 rounded-xl border border-border-default hover:border-border-strong bg-surface-2 hover:bg-surface-3 transition-colors text-left flex items-start gap-4 group"
            >
               <AlertCircle className="w-5 h-5 text-signal-danger shrink-0" />
               <div>
                  <h3 className="font-medium text-primary group-hover:text-primary transition-colors">Track Competitors</h3>
                  <p className="text-xs text-secondary mt-1">Monitor risk profiles and capital movements.</p>
               </div>
            </button>
          </div>
          
          <button 
            onClick={openSearch}
            className="mt-8 flex items-center gap-2 text-sm text-primary font-medium hover:underline"
          >
            Search Intelligence Pipeline <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Watchlist cards would go here */}
        </div>
      )}
    </div>
  );
}
