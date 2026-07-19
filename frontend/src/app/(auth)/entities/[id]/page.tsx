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
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="bg-card">
              <CardHeader>
                <CardTitle className="text-sm font-mono text-muted-foreground uppercase">AI Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed">
                  {entity.recommendation || "No strategic recommendation available for this entity at this time."}
                </p>
                <div className="mt-6 space-y-4">
                  <div className="flex justify-between items-center text-sm border-b border-border pb-2">
                    <span className="text-muted-foreground">Funding Total</span>
                    <span className="font-medium font-mono">${(entity.fundingTotal / 1000000).toFixed(1)}M</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-b border-border pb-2">
                    <span className="text-muted-foreground">Growth Score</span>
                    <span className="font-medium font-mono">{entity.growthScore}/100</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card">
              <CardHeader>
                <CardTitle className="text-sm font-mono text-muted-foreground uppercase flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-signal-danger" />
                  Competitive Threat Level
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <div className="text-2xl font-semibold tracking-tight uppercase text-signal-danger">
                    {entity.riskScore > 75 ? "Critical" : entity.riskScore > 50 ? "High" : "Moderate"}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    Risk score computed as {entity.riskScore}/100 based on recent pipeline analysis.
                  </p>
                </div>
              </CardContent>
            </Card>
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
