"use client";

import { useEffect, useState } from "react";
import { X, Sparkles, TrendingUp, ShieldAlert, Target, Info, ShieldCheck, ArrowRight, ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface AIDecisionCanvasProps {
  isOpen: boolean;
  onClose: () => void;
  entityName: string;
  data: {
    opportunityScore: number;
    riskScore: number;
    momentum: number;
    confidence: number;
    recommendation: string;
    evidence: string[];
  };
}

export function AIDecisionCanvas({ isOpen, onClose, entityName, data }: AIDecisionCanvasProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => { document.body.style.overflow = "unset"; }
  }, [isOpen]);

  if (!isOpen || !mounted) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 sm:p-6 md:p-12 animate-in fade-in duration-200">
      <div 
        className="fixed inset-0 bg-base/90 backdrop-blur-md" 
        onClick={onClose}
      />
      
      <div className="relative w-full max-w-5xl h-full max-h-[85vh] bg-surface-1 border border-border-strong rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in zoom-in-95 duration-300">
        
        {/* Header */}
        <div className="flex items-center justify-between p-6 md:p-8 border-b border-border-default bg-surface-1/50 backdrop-blur-md shrink-0">
          <div>
             <div className="flex items-center gap-3 mb-2">
                <Sparkles className="w-5 h-5 text-signal-positive" />
                <Badge variant="outline" className="font-mono bg-transparent border-primary/20 text-primary">
                  AI Decision Canvas
                </Badge>
             </div>
             <h2 className="text-3xl font-bold tracking-tight text-primary">
               Strategic Posture: {entityName}
             </h2>
          </div>
          <button 
            onClick={onClose}
            className="p-2 text-secondary hover:text-primary rounded-lg hover:bg-surface-2 transition-colors border border-transparent hover:border-border-default"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8">
          
          {/* Top Metrics Row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
             <div className="p-5 rounded-xl border border-border-default bg-surface-2 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-secondary mb-3">
                   <Target className="w-4 h-4 text-signal-positive" />
                   <span className="text-xs font-mono uppercase tracking-wider">Opportunity</span>
                </div>
                <div className="text-3xl font-mono text-primary">{data.opportunityScore}/100</div>
             </div>
             
             <div className="p-5 rounded-xl border border-border-default bg-surface-2 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-secondary mb-3">
                   <ShieldAlert className="w-4 h-4 text-signal-danger" />
                   <span className="text-xs font-mono uppercase tracking-wider">Risk Profile</span>
                </div>
                <div className="text-3xl font-mono text-primary">{data.riskScore}/100</div>
             </div>

             <div className="p-5 rounded-xl border border-border-default bg-surface-2 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-secondary mb-3">
                   <TrendingUp className="w-4 h-4 text-primary" />
                   <span className="text-xs font-mono uppercase tracking-wider">Momentum</span>
                </div>
                <div className="text-3xl font-mono text-primary">{data.momentum}/100</div>
             </div>

             <div className="p-5 rounded-xl border border-border-default bg-surface-2 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-secondary mb-3">
                   <ShieldCheck className="w-4 h-4 text-primary" />
                   <span className="text-xs font-mono uppercase tracking-wider">AI Confidence</span>
                </div>
                <div className="text-3xl font-mono text-primary">{data.confidence}%</div>
             </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
             
             {/* Left Column: Recommendation & Next Actions */}
             <div className="md:col-span-2 space-y-8">
                
                <section>
                   <h3 className="text-lg font-bold text-primary flex items-center gap-2 mb-4">
                      <Sparkles className="w-5 h-5 text-signal-positive" />
                      Strategic Recommendation
                   </h3>
                   <div className="p-6 rounded-xl border border-signal-positive/30 bg-signal-positive/5 leading-relaxed text-primary text-lg">
                      {data.recommendation}
                   </div>
                </section>

                <section>
                   <h3 className="text-lg font-bold text-primary mb-4">Key Evidence & Sources</h3>
                   <div className="space-y-3">
                      {data.evidence.map((ev, i) => (
                         <div key={i} className="p-4 rounded-lg border border-border-default bg-surface-1 flex items-start gap-3">
                            <Info className="w-5 h-5 text-secondary shrink-0 mt-0.5" />
                            <div>
                               <p className="text-sm text-secondary">{ev}</p>
                               <div className="mt-2 flex items-center gap-2">
                                  <span className="text-[10px] font-mono uppercase tracking-widest text-tertiary">Source:</span>
                                  <a href="#" className="text-xs text-primary hover:underline inline-flex items-center gap-1">
                                     Internal Pipeline <ExternalLink className="w-3 h-3" />
                                  </a>
                               </div>
                            </div>
                         </div>
                      ))}
                   </div>
                </section>

             </div>

             {/* Right Column: Actions */}
             <div className="space-y-6">
                <section>
                   <h3 className="text-sm font-mono uppercase tracking-wider text-secondary mb-4">Suggested Next Actions</h3>
                   <div className="space-y-3">
                      <button className="w-full flex items-center justify-between p-4 rounded-xl border border-border-default bg-surface-2 hover:bg-surface-3 transition-colors text-left group">
                         <div>
                            <div className="text-sm font-medium text-primary">Generate Brief</div>
                            <div className="text-xs text-secondary mt-1">Export full analyst report</div>
                         </div>
                         <ArrowRight className="w-4 h-4 text-tertiary group-hover:text-primary transition-colors" />
                      </button>
                      
                      <button className="w-full flex items-center justify-between p-4 rounded-xl border border-border-default bg-surface-2 hover:bg-surface-3 transition-colors text-left group">
                         <div>
                            <div className="text-sm font-medium text-primary">Compare Competitors</div>
                            <div className="text-xs text-secondary mt-1">Map against market leaders</div>
                         </div>
                         <ArrowRight className="w-4 h-4 text-tertiary group-hover:text-primary transition-colors" />
                      </button>

                      <button className="w-full flex items-center justify-between p-4 rounded-xl border border-primary/30 bg-primary/10 hover:bg-primary/20 transition-colors text-left group">
                         <div>
                            <div className="text-sm font-medium text-primary">Monitor Entity</div>
                            <div className="text-xs text-primary/70 mt-1">Alert on material changes</div>
                         </div>
                         <ArrowRight className="w-4 h-4 text-primary transition-colors" />
                      </button>
                   </div>
                </section>
             </div>

          </div>

        </div>
      </div>
    </div>
  );
}
