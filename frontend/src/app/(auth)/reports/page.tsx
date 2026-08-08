"use client";

import { useRecommendations } from "@/hooks/use-intelligence";
import { Badge } from "@/components/ui/badge";
import { Loader2, FileText, CheckCircle, ShieldAlert, Target, TrendingUp, BarChart3, Clock, AlertTriangle, Zap } from "lucide-react";
import { useRouter } from "next/navigation";

export default function ReportsPage() {
  const { data: recommendations, isLoading, isError } = useRecommendations();
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-6">
          <div className="relative">
             <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full"></div>
             <Loader2 className="w-12 h-12 text-primary animate-spin relative z-10" />
          </div>
          <p className="text-muted-foreground font-mono tracking-widest uppercase text-sm animate-pulse">Generating Analyst Reports...</p>
        </div>
      </div>
    );
  }

  if (isError || !recommendations) {
    return (
      <div className="h-full flex items-center justify-center min-h-[50vh]">
        <div className="text-red-400 bg-red-400/10 p-4 rounded-lg border border-red-400/20 font-mono text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" /> Failed to connect to intelligence engine.
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-10 flex flex-col pb-20">
      {/* Header Section */}
      <div className="flex justify-between items-end shrink-0 border-b border-border/50 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-xs font-mono uppercase tracking-widest text-primary font-semibold">Alpha Intelligence</span>
          </div>
          <h1 className="text-4xl font-heading font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">Strategic Reports</h1>
          <p className="text-muted-foreground mt-2 max-w-2xl text-lg leading-relaxed">
            AI-generated market deep-dives, strategic playbooks, and algorithmic capital allocation recommendations based on real-time ecosystem monitoring.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 space-y-8">
        {recommendations.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center border border-border/30 rounded-2xl bg-surface-1/50 backdrop-blur-xl p-16 text-center shadow-2xl">
             <div className="w-20 h-20 bg-surface-2 rounded-2xl flex items-center justify-center text-secondary mb-6 shadow-inner ring-1 ring-white/5">
                <FileText className="w-10 h-10" />
             </div>
             <h2 className="text-2xl font-bold text-primary mb-2">Awaiting Signals</h2>
             <p className="text-secondary max-w-md mx-auto leading-relaxed mb-8">
                The intelligence engine is actively monitoring your watchlist. Strategic reports will generate automatically when market anomalies or high-probability events are detected.
             </p>
             <button 
               onClick={() => router.push('/watchlist')}
               className="px-8 py-3 bg-primary text-primary-foreground hover:bg-primary/90 rounded-full text-sm font-bold tracking-wide transition-all shadow-lg hover:shadow-primary/25 hover:-translate-y-0.5"
             >
               Configure Watchlist
             </button>
          </div>
        ) : (
          recommendations.map((rec) => (
            <div key={rec.id} className="relative group">
              {/* Premium Glow Effect behind card */}
              <div className={`absolute -inset-0.5 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000 group-hover:duration-200 ${
                rec.priority === 'Critical' ? 'bg-signal-danger' : 
                rec.priority === 'High' ? 'bg-primary' : 
                'bg-blue-500'
              }`}></div>
              
              <div className="relative bg-[#0c0c0e] border border-white/5 rounded-2xl overflow-hidden shadow-2xl">
                
                {/* Card Header Banner */}
                <div className={`px-8 py-5 border-b flex items-center justify-between ${
                  rec.priority === 'Critical' ? 'bg-signal-danger/10 border-signal-danger/20' : 
                  rec.priority === 'High' ? 'bg-primary/10 border-primary/20' : 
                  'bg-white/5 border-white/5'
                }`}>
                  <div className="flex items-center gap-4">
                    <Badge variant="outline" className={`font-mono text-xs uppercase tracking-wider px-3 py-1 ${
                      rec.priority === 'Critical' ? 'text-signal-danger border-signal-danger/40 bg-signal-danger/10' :
                      rec.priority === 'High' ? 'text-primary border-primary/40 bg-primary/10' :
                      'text-muted-foreground border-white/10'
                    }`}>
                      {rec.priority} Priority
                    </Badge>
                    <div className="flex items-center gap-1.5 text-xs text-muted-foreground font-mono">
                      <Clock className="w-3.5 h-3.5" />
                      {new Date(rec.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <div className="text-[10px] uppercase font-mono tracking-widest text-muted-foreground">Conviction</div>
                      <div className="font-mono font-bold text-lg text-white">{rec.confidence}%</div>
                    </div>
                    <div className="h-8 w-8 rounded-full border border-white/10 flex items-center justify-center bg-white/5">
                       <BarChart3 className="w-4 h-4 text-white" />
                    </div>
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-8">
                  <h3 className="text-2xl font-bold font-heading text-white mb-4 leading-tight">{rec.title}</h3>
                  <p className="text-muted-foreground text-lg leading-relaxed mb-8">{rec.reason}</p>
                  
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    
                    {/* Left Column: Action & Impact */}
                    <div className="lg:col-span-7 space-y-6">
                      <div className="bg-surface-2/50 border border-white/5 rounded-xl p-5 backdrop-blur-sm">
                        <h4 className="text-xs font-mono uppercase tracking-widest text-primary mb-3 flex items-center gap-2">
                          <Target className="w-4 h-4" /> Recommended Action
                        </h4>
                        <p className="text-white text-base leading-relaxed">{rec.suggestedAction}</p>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="border border-signal-positive/20 bg-signal-positive/5 rounded-xl p-5">
                          <h4 className="text-xs font-mono uppercase tracking-widest text-signal-positive mb-2 flex items-center gap-2">
                            <TrendingUp className="w-4 h-4" /> Opportunity
                          </h4>
                          <p className="text-sm text-foreground/80 leading-relaxed font-medium">{rec.estimatedOpportunity}</p>
                        </div>
                        <div className="border border-signal-danger/20 bg-signal-danger/5 rounded-xl p-5">
                          <h4 className="text-xs font-mono uppercase tracking-widest text-signal-danger mb-2 flex items-center gap-2">
                            <ShieldAlert className="w-4 h-4" /> Downside Risk
                          </h4>
                          <p className="text-sm text-foreground/80 leading-relaxed font-medium">{rec.estimatedRisk}</p>
                        </div>
                      </div>
                    </div>

                    {/* Right Column: Evidence */}
                    <div className="lg:col-span-5 border-l border-white/5 pl-8">
                      <h4 className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-4 flex items-center gap-2">
                        <CheckCircle className="w-4 h-4" /> Synthesized Evidence
                      </h4>
                      <ul className="space-y-4">
                        {rec.evidence.map((ev, i) => (
                          <li key={i} className="flex gap-3 text-sm text-muted-foreground leading-relaxed">
                            <span className="w-1.5 h-1.5 rounded-full bg-primary/60 shrink-0 mt-1.5"></span>
                            <span>{ev}</span>
                          </li>
                        ))}
                      </ul>
                      
                      {rec.relatedCompanies && rec.relatedCompanies.length > 0 && (
                        <div className="mt-8 pt-6 border-t border-white/5">
                          <h4 className="text-[10px] font-mono uppercase tracking-widest text-muted-foreground mb-3">Implicated Entities</h4>
                          <div className="flex flex-wrap gap-2">
                            {rec.relatedCompanies.map(company => (
                              <span key={company} className="px-2.5 py-1 rounded bg-white/5 border border-white/10 text-xs font-medium text-white/80">
                                {company}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
