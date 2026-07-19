"use client";

import { Search, ArrowRight, Activity, Zap, ShieldAlert, LineChart } from "lucide-react";
import { useRouter } from "next/navigation";
import { TopBar } from "@/components/layout/topbar";

export default function LandingPage() {
  const router = useRouter();

  const handleSearchClick = () => {
    // Trigger the OmniSearchDialog (Cmd+K)
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', metaKey: true }));
  };

  const suggestedEntities = [
    { name: "OpenAI", icon: Zap, color: "text-blue-400" },
    { name: "Anthropic", icon: Activity, color: "text-purple-400" },
    { name: "Perplexity", icon: Search, color: "text-teal-400" },
    { name: "Mistral", icon: LineChart, color: "text-orange-400" },
    { name: "Stripe", icon: ShieldAlert, color: "text-indigo-400" },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <TopBar />
      
      <main className="flex-1 flex flex-col items-center justify-center p-6 text-center">
        <div className="max-w-4xl mx-auto space-y-12">
          
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-1000">
            <h1 className="text-5xl md:text-7xl font-bold tracking-tighter text-foreground">
              Monitor any startup.<br/>
              <span className="text-muted-foreground">Understand what changed.</span><br/>
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-500">
                Know what to do next.
              </span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto font-mono">
              The AI-powered strategic decision platform. Enter any entity to instantly generate a complete intelligence brief.
            </p>
          </div>

          <div className="max-w-2xl mx-auto relative animate-in fade-in slide-in-from-bottom-12 duration-1000 delay-150">
            <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-blue-500/20 blur-xl rounded-full" />
            <button 
              onClick={handleSearchClick}
              className="relative w-full bg-card border border-border hover:border-primary/50 transition-all duration-300 rounded-full p-4 pl-6 pr-4 flex items-center gap-4 group shadow-2xl"
            >
              <Search className="w-6 h-6 text-muted-foreground group-hover:text-primary transition-colors" />
              <div className="flex-1 text-left text-lg text-muted-foreground font-sans">
                Search a startup...
              </div>
              <div className="flex items-center gap-2">
                <kbd className="hidden sm:inline-flex h-8 items-center gap-1 rounded-full border border-border bg-muted px-3 font-mono text-xs font-medium text-muted-foreground">
                  ⌘K
                </kbd>
                <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-primary-foreground group-hover:scale-105 transition-transform">
                  <ArrowRight className="w-5 h-5" />
                </div>
              </div>
            </button>
          </div>

          <div className="pt-12 animate-in fade-in slide-in-from-bottom-16 duration-1000 delay-300">
            <p className="text-sm font-mono tracking-widest uppercase text-muted-foreground mb-6">Suggested Entities</p>
            <div className="flex flex-wrap justify-center gap-4">
              {suggestedEntities.map((entity) => (
                <button 
                  key={entity.name}
                  onClick={() => router.push('/dashboard')}
                  className="flex items-center gap-2 px-6 py-3 rounded-full border border-border bg-card hover:bg-accent hover:border-border-strong transition-all"
                >
                  <entity.icon className={`w-4 h-4 ${entity.color}`} />
                  <span className="font-medium">{entity.name}</span>
                </button>
              ))}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
