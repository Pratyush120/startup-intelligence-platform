"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Search, ArrowRight, Sparkles, Building2, TrendingUp, Loader2 } from "lucide-react";
import { useUIStore } from "@/store/ui.store";
import { useSearch } from "@/hooks/use-intelligence";
import { CompanyMetric } from "@/lib/types/executive";

export function CommandPalette() {
  const { isSearchOpen, closeSearch } = useUIStore();
  const [query, setQuery] = useState("");
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const { data: searchResults, isLoading } = useSearch(query);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        useUIStore.getState().toggleSearch();
      }
      if (e.key === "Escape" && useUIStore.getState().isSearchOpen) {
        useUIStore.getState().closeSearch();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  useEffect(() => {
    if (isSearchOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery("");
    }
  }, [isSearchOpen]);

  if (!isSearchOpen) return null;

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      closeSearch();
      useUIStore.getState().openCopilot(); // Default action: route to AI Copilot
    }
  };

  const handleSelectEntity = (entityName: string) => {
    closeSearch();
    router.push(`/entities/${encodeURIComponent(entityName)}`);
  };

  const suggestions = [
    { icon: <Building2 className="w-4 h-4" />, text: "Analyze OpenAI" },
    { icon: <TrendingUp className="w-4 h-4" />, text: "Compare Stripe vs Adyen" },
    { icon: <Search className="w-4 h-4" />, text: "Healthcare AI startups" },
    { icon: <Sparkles className="w-4 h-4" />, text: "Why is Cursor growing?" },
  ];

  return (
    <div className="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh] sm:pt-[20vh] px-4">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-base/80 backdrop-blur-sm transition-opacity" 
        onClick={closeSearch}
      />
      
      {/* Palette */}
      <div className="relative w-full max-w-2xl bg-surface-1 border border-border-default rounded-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        <form onSubmit={handleSearch} className="relative flex items-center px-4 py-4 border-b border-border-default">
          <Search className="w-5 h-5 text-secondary shrink-0" />
          <input
            ref={inputRef}
            type="text"
            className="flex-1 bg-transparent border-none outline-none text-primary px-4 text-lg placeholder:text-tertiary"
            placeholder="Analyze a company, market or competitor..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <kbd className="hidden sm:inline-flex items-center gap-1 rounded border border-border-default bg-surface-2 px-2 py-1 font-mono text-[10px] font-medium text-secondary">
            ESC
          </kbd>
        </form>

        <div className="p-4 overflow-y-auto max-h-[50vh]">
          {!query ? (
            <div className="space-y-4">
              <h3 className="text-xs font-mono uppercase tracking-wider text-secondary px-2">Suggested Actions</h3>
              <div className="space-y-1">
                {suggestions.map((s, i) => (
                  <button
                    key={i}
                    className="w-full flex items-center gap-3 px-3 py-3 rounded-lg text-left text-primary hover:bg-surface-2 transition-colors group"
                    onClick={() => {
                       setQuery(s.text);
                       // Defer to next tick so setQuery has flushed, then fire handleSearch
                       setTimeout(() => {
                         const syntheticEvent = { preventDefault: () => {} } as React.FormEvent;
                         handleSearch(syntheticEvent);
                       }, 100);
                    }}
                  >
                    <div className="text-secondary group-hover:text-primary transition-colors">
                      {s.icon}
                    </div>
                    <span className="flex-1">{s.text}</span>
                    <ArrowRight className="w-4 h-4 text-tertiary group-hover:text-primary opacity-0 group-hover:opacity-100 transition-all -translate-x-2 group-hover:translate-x-0" />
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {isLoading ? (
                <div className="flex items-center justify-center p-4">
                  <Loader2 className="w-5 h-5 animate-spin text-secondary" />
                </div>
              ) : (searchResults?.companies && searchResults.companies.length > 0) ? (
                <div className="space-y-2">
                  <h3 className="text-xs font-mono uppercase tracking-wider text-secondary px-2">Companies</h3>
                  {searchResults.companies.map((company: CompanyMetric) => (
                    <button
                      key={company.id || company.name}
                      onClick={() => handleSelectEntity(company.name)}
                      className="w-full flex items-center justify-between gap-3 px-3 py-3 rounded-lg text-left text-primary hover:bg-surface-2 transition-colors border border-transparent hover:border-border-default"
                    >
                      <div className="flex items-center gap-3">
                        <Building2 className="w-4 h-4 text-secondary" />
                        <span className="font-medium">{company.name}</span>
                      </div>
                      <span className="text-xs font-mono text-tertiary">Score: {company.growthScore}</span>
                    </button>
                  ))}
                </div>
              ) : null}

              <div className="space-y-2 border-t border-border-default pt-4">
                <button
                  className="w-full flex items-center gap-3 px-3 py-3 rounded-lg text-left text-primary hover:bg-surface-2 transition-colors bg-surface-2/50 border border-border-default"
                  onClick={handleSearch}
                >
                  <Sparkles className="w-4 h-4 text-signal-positive" />
                  <span className="flex-1">Ask AI Copilot to analyze: <strong>"{query}"</strong></span>
                  <kbd className="hidden sm:inline-flex items-center gap-1 rounded border border-border-strong bg-surface-3 px-2 py-1 font-mono text-[10px] font-medium text-primary">
                    ENTER
                  </kbd>
                </button>
              </div>
            </div>
          )}
        </div>
        
      </div>
    </div>
  );
}
