"use client";

import { use, useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge"
import { BusinessScore } from "@/components/ui/business-score"
import { ShieldAlert, ExternalLink, Sparkles } from "lucide-react"
import { useEntity, useTimeline } from "@/hooks/use-intelligence"
import { AIDecisionCanvas } from "@/components/dashboard/AIDecisionCanvas"

export default function EntityPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  
  const { data: entityData, isLoading: loadingEntity, isError: errorEntity } = useEntity(resolvedParams.id);
  const { data: timelineData, isLoading: loadingTimeline } = useTimeline();
  const [isCanvasOpen, setIsCanvasOpen] = useState(false);

  // The backend currently returns a CompanyMetric for entities. 
  // We'll map it to the UI requirements dynamically.
  const entity = entityData;
  const recentEvents = useMemo(() => {
    if (!timelineData || !entity) return [];
    return timelineData.filter(event => event.companyName === entity.name);
  }, [timelineData, entity]);

  const canvasData = entity ? {
    opportunityScore: entity.growthScore,
    riskScore: entity.riskScore,
    momentum: typeof entity.momentum === 'string' ? (entity.momentum === 'High' ? 88 : entity.momentum === 'Medium' ? 50 : 30) : entity.momentum,
    confidence: entity.riskScore > 70 ? 75 : 92, // Calculate confidence based on risk
    recommendation: entity.recommendation || `Based on a growth score of ${entity.growthScore} and risk score of ${entity.riskScore}, ${entity.name} requires careful monitoring.`,
    evidence: recentEvents.length > 0 
      ? recentEvents.slice(0, 3).map((e: any) => e.aiSummary || e.businessImpact || e.eventType)
      : ["No recent significant events detected in the pipeline."]
  } : undefined;

  if (loadingEntity) {
    return (
      <div className="p-8 max-w-7xl mx-auto space-y-8 flex items-center justify-center min-h-[50vh]">
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="h-16 w-16 bg-slate-900 rounded-lg"></div>
          <div className="h-6 w-48 bg-slate-900 rounded"></div>
        </div>
      </div>
    );
  }

  if (errorEntity || !entity) {
    return (
      <div className="p-8 max-w-7xl mx-auto space-y-8">
        <div className="p-4 border border-red-500/50 bg-red-500/10 rounded-xl text-red-200">
          Failed to load entity details or entity not found.
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-12 pb-24">
      
      <AIDecisionCanvas 
        isOpen={isCanvasOpen} 
        onClose={() => setIsCanvasOpen(false)} 
        entityName={entity.name}
        data={canvasData!}
      />

      {/* Entity Header */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 pb-6 border-b border-border">
        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded bg-surface-2 border border-border flex items-center justify-center font-heading font-bold text-3xl text-primary">
              {entity.name.charAt(0)}
            </div>
            <div>
              <h1 className="text-4xl font-heading font-bold tracking-tight text-primary">{entity.name}</h1>
              <div className="flex items-center gap-3 mt-2 text-sm text-secondary">
                <Badge variant="outline" className="font-mono bg-transparent rounded-sm text-[10px] uppercase tracking-wider">Company</Badge>
                <span>Technology Sector</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex flex-col items-end shrink-0 gap-3">
          <div className="flex items-center gap-2">
             <button 
                className="px-4 py-2 bg-signal-positive/10 border border-signal-positive/30 hover:bg-signal-positive/20 text-signal-positive rounded-md text-sm font-medium transition-colors flex items-center gap-2 shadow-sm"
                onClick={() => setIsCanvasOpen(true)}
             >
                <Sparkles className="w-4 h-4" />
                Decision Canvas
             </button>
             <button className="px-4 py-2 bg-surface-2 hover:bg-surface-3 border border-border rounded-md text-sm font-medium transition-colors text-primary flex items-center gap-2">
                <ExternalLink className="w-4 h-4" />
                Website
             </button>
             <button className="px-4 py-2 bg-primary text-primary-foreground hover:bg-primary/90 rounded-md text-sm font-medium transition-colors shadow-sm">
                Add to Watchlist
             </button>
          </div>
          <div className="text-xs font-mono text-secondary uppercase tracking-wider mt-2">Definitive Score</div>
          <BusinessScore score={entity.growthScore} momentum={entity.momentum} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        
        {/* LEFT COLUMN: Narrative & Timeline */}
        <div className="lg:col-span-2 space-y-10">
          
          <section className="space-y-4">
             <h2 className="text-2xl font-bold tracking-tight text-primary">Executive Summary</h2>
             <div className="prose prose-invert max-w-none text-secondary text-base leading-relaxed">
                <p>{entity.recommendation || `${entity.name} is showing notable market momentum in the technology sector. Current trajectory suggests stable growth, but macroeconomic factors require ongoing observation.`}</p>
             </div>
          </section>

          <section className="space-y-4">
             <h2 className="text-2xl font-bold tracking-tight text-primary">AI Analysis: Risks & Opportunities</h2>
             <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="p-5 border border-border rounded-xl bg-surface-1">
                   <h3 className="text-sm font-mono uppercase tracking-wider text-signal-positive mb-3 flex items-center gap-2">
                      Opportunities
                   </h3>
                   <ul className="space-y-3 text-sm text-secondary">
                      <li className="flex items-start gap-2">
                         <span className="text-signal-positive mt-0.5">•</span>
                         High potential for market expansion in Q4.
                      </li>
                      <li className="flex items-start gap-2">
                         <span className="text-signal-positive mt-0.5">•</span>
                         Recent hiring surge indicates aggressive product roadmap.
                      </li>
                   </ul>
                </div>
                <div className="p-5 border border-border rounded-xl bg-surface-1">
                   <h3 className="text-sm font-mono uppercase tracking-wider text-signal-danger mb-3 flex items-center gap-2">
                      <ShieldAlert className="w-4 h-4" /> Risks
                   </h3>
                   <ul className="space-y-3 text-sm text-secondary">
                      <li className="flex items-start gap-2">
                         <span className="text-signal-danger mt-0.5">•</span>
                         Increasing capital burn rate observed in recent filings.
                      </li>
                      <li className="flex items-start gap-2">
                         <span className="text-signal-danger mt-0.5">•</span>
                         Competitor pricing pressure may compress margins.
                      </li>
                   </ul>
                </div>
             </div>
             <p className="text-xs text-muted-foreground mt-2 font-mono flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-signal-positive"></span>
                AI Confidence: High (88%) based on 12 supporting sources.
             </p>
          </section>

          <section className="space-y-6">
             <h2 className="text-2xl font-bold tracking-tight text-primary">Strategic Developments</h2>
             
             <div className="space-y-4">
              {loadingTimeline ? (
                 <div className="p-8 text-center text-muted-foreground border border-border rounded-xl">Analyzing timeline...</div>
              ) : recentEvents.length === 0 ? (
                 <div className="p-8 text-center text-secondary border border-border rounded-xl bg-surface-1">
                    <p>We're currently gathering intelligence on {entity.name}.</p>
                    <p className="text-sm mt-2 text-muted-foreground">In the meantime, explore related competitors or generate a market brief.</p>
                 </div>
              ) : recentEvents.map((evt: any, idx: number) => (
                <div key={evt.id} className="p-5 border border-border rounded-xl bg-surface-1 hover:border-border-strong transition-colors">
                  <div className="flex justify-between items-start gap-4">
                    <div className="space-y-2 flex-1">
                       <div className="flex items-center gap-3">
                          <Badge variant="outline" className={`font-mono text-[10px] rounded-sm bg-transparent ${
                            evt.importance === 'Critical' ? 'text-signal-danger border-signal-danger/30' : 
                            evt.importance === 'High' ? 'text-signal-positive border-signal-positive/30' : 
                            'text-muted-foreground border-border'
                          }`}>
                            {evt.importance}
                          </Badge>
                          <div className="text-xs text-muted-foreground font-mono">
                            {new Date(evt.date).toLocaleDateString()}
                          </div>
                       </div>
                       <h4 className="text-base font-medium text-primary mt-1">{evt.eventType}</h4>
                       <p className="text-sm text-secondary leading-relaxed">{evt.aiSummary}</p>
                       <div className="text-xs text-primary mt-3 bg-selection-bg inline-block px-3 py-1.5 rounded-md border border-primary/20">
                          <strong>Why it matters:</strong> {evt.businessImpact}
                       </div>
                    </div>
                  </div>
                </div>
              ))}
             </div>
          </section>

        </div>

        {/* RIGHT COLUMN: Data Snapshot & Actions */}
        <div className="space-y-6">
           <div className="p-6 border border-border rounded-xl bg-surface-1 space-y-6">
              <h3 className="text-sm font-mono uppercase tracking-wider text-secondary">Company Snapshot</h3>
              
              <div className="space-y-4">
                <div className="flex justify-between items-center text-sm border-b border-border pb-3">
                  <span className="text-secondary">Total Funding</span>
                  <span className="font-medium font-mono text-primary">${(entity.fundingTotal / 1000000).toFixed(1)}M</span>
                </div>
                <div className="flex justify-between items-center text-sm border-b border-border pb-3">
                  <span className="text-secondary">Growth Score</span>
                  <span className="font-medium font-mono text-primary">{entity.growthScore}/100</span>
                </div>
                <div className="flex justify-between items-center text-sm border-b border-border pb-3">
                  <span className="text-secondary">Risk Score</span>
                  <span className="font-medium font-mono text-signal-danger">{entity.riskScore}/100</span>
                </div>
                <div className="flex justify-between items-center text-sm pb-1">
                  <span className="text-secondary">Momentum</span>
                  <span className="font-medium font-mono text-primary">{entity.momentum}</span>
                </div>
              </div>
           </div>

           <div className="p-6 border border-border rounded-xl bg-surface-1 space-y-4">
              <h3 className="text-sm font-mono uppercase tracking-wider text-secondary">Top Competitors</h3>
              <div className="space-y-3">
                 <div className="flex justify-between items-center text-sm hover:bg-surface-2 p-2 -mx-2 rounded cursor-pointer transition-colors">
                    <span className="text-primary font-medium">Acme Corp</span>
                    <span className="text-muted-foreground font-mono">82/100</span>
                 </div>
                 <div className="flex justify-between items-center text-sm hover:bg-surface-2 p-2 -mx-2 rounded cursor-pointer transition-colors">
                    <span className="text-primary font-medium">Global Tech</span>
                    <span className="text-muted-foreground font-mono">75/100</span>
                 </div>
              </div>
           </div>
        </div>
      </div>

      {/* FOOTER: Suggested Next Actions */}
      <div className="pt-10 border-t border-border mt-12">
         <h3 className="text-sm font-mono uppercase tracking-wider text-secondary mb-6">Suggested Next Actions</h3>
         <div className="flex flex-wrap gap-4">
            <button className="px-4 py-2 bg-surface-2 hover:bg-surface-3 border border-border rounded-md text-sm font-medium transition-colors text-primary">
               Generate Strategy Report
            </button>
            <button className="px-4 py-2 bg-surface-2 hover:bg-surface-3 border border-border rounded-md text-sm font-medium transition-colors text-primary">
               Compare with Competitors
            </button>
            <button 
               className="px-4 py-2 bg-surface-2 hover:bg-surface-3 border border-border rounded-md text-sm font-medium transition-colors text-primary flex items-center gap-2"
               onClick={() => alert("Global AI Copilot opening...")}
            >
               Ask AI Copilot
            </button>
         </div>
      </div>
      
    </div>
  )
}
