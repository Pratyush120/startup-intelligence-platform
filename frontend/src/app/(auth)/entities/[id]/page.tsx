"use client";

import { use, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { BusinessScore } from "@/components/ui/business-score"
import { ShieldAlert, ExternalLink, Star } from "lucide-react"
import { useEntity, useTimeline } from "@/hooks/use-intelligence"
import { useWatchlistStore } from "@/stores/watchlist.store"

export default function EntityPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  
  const { data: entityData, isLoading: loadingEntity, isError: errorEntity } = useEntity(resolvedParams.id);
  const { data: timelineData, isLoading: loadingTimeline } = useTimeline();
  
  const isWatched = useWatchlistStore((state) => state.isWatched(entityData?.name || ''));
  const addEntity = useWatchlistStore((state) => state.addEntity);
  const removeEntity = useWatchlistStore((state) => state.removeEntity);

  // The backend currently returns a CompanyMetric for entities. 
  // We'll map it to the UI requirements dynamically.
  const entity = entityData;
  const recentEvents = useMemo(() => {
    if (!timelineData || !entity) return [];
    return timelineData.filter(event => event.companyName === entity.name);
  }, [timelineData, entity]);

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
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      
      {/* Entity Header */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 pb-6 border-b border-border">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded bg-muted border border-border flex items-center justify-center font-heading font-bold text-xl">
              {entity.name.charAt(0)}
            </div>
            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-3xl font-heading font-semibold tracking-tight">{entity.name}</h1>
                <button 
                  onClick={() => isWatched ? removeEntity(entity.name) : addEntity(entity.name)}
                  className={`p-2 rounded-full transition-colors ${isWatched ? 'text-yellow-500 bg-yellow-500/10 hover:bg-yellow-500/20' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}`}
                  title={isWatched ? "Remove from watchlist" : "Add to watchlist"}
                >
                  <Star className={`w-5 h-5 ${isWatched ? 'fill-current' : ''}`} />
                </button>
              </div>
              <div className="flex items-center gap-2 mt-1 text-sm text-muted-foreground">
                <Badge variant="outline" className="font-mono bg-transparent rounded-sm text-[10px]">Company</Badge>
                <span>Technology</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex flex-col items-end shrink-0">
          <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider mb-1">Definitive Score</div>
          <BusinessScore score={entity.growthScore} momentum={entity.momentum} />
        </div>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="bg-transparent border-b border-border w-full justify-start rounded-none h-auto p-0 space-x-6">
          <TabsTrigger value="overview" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-foreground rounded-none border-b-2 border-transparent px-0 py-3 text-sm font-medium transition-none">
            Overview
          </TabsTrigger>
          <TabsTrigger value="intelligence" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-foreground rounded-none border-b-2 border-transparent px-0 py-3 text-sm font-medium transition-none">
            Intelligence Mechanics
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="overview" className="mt-8 space-y-8">
          
          {/* Executive Overview Section */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-3 space-y-6">
               <Card className="bg-card">
                 <CardHeader>
                   <CardTitle className="text-sm font-mono text-muted-foreground uppercase flex items-center gap-2">
                     <Star className="w-4 h-4 text-primary" /> AI Strategy Analysis
                   </CardTitle>
                 </CardHeader>
                 <CardContent>
                   <p className="text-lg leading-relaxed text-foreground">
                     {entity.recommendation || "Monitoring required to generate strategic recommendation."}
                   </p>
                   <div className="mt-4 p-4 bg-muted/20 border border-border rounded-md">
                      <h4 className="text-sm font-semibold mb-2">Why this matters</h4>
                      <p className="text-sm text-muted-foreground">
                        The current growth score of {entity.growthScore} and momentum of {entity.momentum} indicates a {entity.trendDirection} trajectory. 
                        Combined with a risk score of {entity.riskScore}, this implies significant business implications for competitors in the sector.
                      </p>
                   </div>
                 </CardContent>
               </Card>

               <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                 <div className="p-4 bg-card border border-border rounded-lg">
                   <div className="text-xs font-mono text-muted-foreground uppercase mb-1">Latest Funding</div>
                   <div className="text-2xl font-bold">${(entity.fundingTotal / 1000000).toFixed(1)}M</div>
                   <div className="text-xs text-signal-positive mt-1">+12% vs previous round</div>
                 </div>
                 <div className="p-4 bg-card border border-border rounded-lg">
                   <div className="text-xs font-mono text-muted-foreground uppercase mb-1">Est. Valuation</div>
                   <div className="text-2xl font-bold">${((entity.fundingTotal * 8) / 1000000).toFixed(1)}M</div>
                   <div className="text-xs text-muted-foreground mt-1">Based on market multiples</div>
                 </div>
                 <div className="p-4 bg-card border border-border rounded-lg">
                   <div className="text-xs font-mono text-muted-foreground uppercase mb-1">Hiring Trend</div>
                   <div className="text-2xl font-bold text-signal-positive">Accelerating</div>
                   <div className="text-xs text-muted-foreground mt-1">15 open executive roles</div>
                 </div>
               </div>
            </div>

            <div className="space-y-4">
               <div className="p-4 bg-muted/10 border border-border rounded-lg space-y-4">
                  <h3 className="text-sm font-semibold border-b border-border pb-2">Company Profile</h3>
                  <div>
                    <div className="text-xs text-muted-foreground mb-1">Industry</div>
                    <div className="text-sm font-medium">Artificial Intelligence</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground mb-1">Founding Year</div>
                    <div className="text-sm font-medium">2019</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground mb-1">Employees</div>
                    <div className="text-sm font-medium">500 - 1,000</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground mb-1">Headquarters</div>
                    <div className="text-sm font-medium">San Francisco, CA</div>
                  </div>
               </div>
               
               <div className="p-4 bg-card border border-signal-danger/30 rounded-lg">
                  <div className="text-xs font-mono text-signal-danger uppercase mb-1 flex items-center gap-2">
                    <ShieldAlert className="w-3 h-3" /> Risk Level
                  </div>
                  <div className="text-xl font-bold text-signal-danger">
                    {entity.riskScore > 75 ? "Critical" : entity.riskScore > 50 ? "High" : "Moderate"}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">Score: {entity.riskScore}/100</div>
               </div>
            </div>
          </div>

        </TabsContent>

        <TabsContent value="intelligence" className="mt-8 space-y-6">
           <h3 className="text-lg font-medium tracking-tight">Extracted News & Events</h3>
           <div className="border border-border rounded-md overflow-hidden bg-card">
              {loadingTimeline ? (
                 <div className="p-8 text-center text-muted-foreground">Analyzing timeline...</div>
              ) : recentEvents.length === 0 ? (
                 <div className="p-8 text-center text-muted-foreground">No recent events detected for this entity.</div>
              ) : recentEvents.map((evt: any, idx: number) => (
                <div key={evt.id} className={`p-4 ${idx !== recentEvents.length - 1 ? 'border-b border-border' : ''} hover:bg-muted/30 transition-colors`}>
                  <div className="flex justify-between items-start gap-4">
                    <div className="space-y-1 flex-1">
                       <div className="text-sm font-medium">{evt.eventType}</div>
                       <div className="text-xs text-muted-foreground">{evt.aiSummary}</div>
                       <div className="text-xs text-muted-foreground mt-2 border-l-2 border-primary/50 pl-2">
                          Impact: {evt.businessImpact}
                       </div>
                    </div>
                    <div className="flex flex-col items-end shrink-0 space-y-2">
                      <Badge variant="outline" className={`font-mono text-[10px] rounded-sm bg-transparent ${
                        evt.importance === 'Critical' ? 'text-signal-danger border-signal-danger/30' : 
                        evt.importance === 'High' ? 'text-signal-positive border-signal-positive/30' : 
                        'text-muted-foreground border-border'
                      }`}>
                        Importance: {evt.importance}
                      </Badge>
                      <div className="text-xs text-muted-foreground font-mono flex items-center gap-1">
                        <ExternalLink className="w-3 h-3" /> {new Date(evt.date).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
           </div>
        </TabsContent>
      </Tabs>
      
    </div>
  )
}
