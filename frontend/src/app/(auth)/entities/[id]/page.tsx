import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { mockEntities } from "@/lib/mockData"
import { BusinessScore } from "@/components/ui/business-score"
import { ShieldAlert, TrendingUp, Search, ExternalLink } from "lucide-react"

export default function EntityPage() {
  // Hardcoded for demonstration, normally fetched via params.id
  const entity = mockEntities[0];
  if (!entity) return null;

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
              <h1 className="text-3xl font-heading font-semibold tracking-tight">{entity.name}</h1>
              <div className="flex items-center gap-2 mt-1 text-sm text-muted-foreground">
                <Badge variant="outline" className="font-mono bg-transparent rounded-sm text-[10px]">{entity.type}</Badge>
                <span>{entity.sector}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex flex-col items-end shrink-0">
          <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider mb-1">Definitive Score</div>
          <BusinessScore score={entity.score.overall} momentum={entity.score.momentum} />
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
                  {entity.description}
                </p>
                <div className="mt-6 space-y-4">
                  <div className="flex justify-between items-center text-sm border-b border-border pb-2">
                    <span className="text-muted-foreground">Market Position</span>
                    <span className="font-medium font-mono">{entity.score.marketPosition}/100</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-b border-border pb-2">
                    <span className="text-muted-foreground">Financial Health</span>
                    <span className="font-medium font-mono">{entity.score.financialHealth}/100</span>
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
                    {entity.score.threatLevel}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    Based on aggressive mid-market expansion and recent funding rounds.
                  </p>
                </div>
                <div>
                  <h4 className="text-xs font-mono text-muted-foreground uppercase mb-2">Identified Competitors</h4>
                  <div className="flex flex-wrap gap-2">
                    {entity.competitors.map((comp: any) => (
                       <Badge key={comp} variant="secondary" className="rounded-sm bg-muted text-foreground">Ent-Auto-Log</Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

        </TabsContent>

        <TabsContent value="intelligence" className="mt-8 space-y-6">
           <h3 className="text-lg font-medium tracking-tight">Extracted News Sentiment</h3>
           <div className="border border-border rounded-md overflow-hidden bg-card">
              {entity.recentEvents.map((evt: any, idx: number) => (
                <div key={evt.id} className={`p-4 ${idx !== entity.recentEvents.length - 1 ? 'border-b border-border' : ''} hover:bg-muted/30 transition-colors`}>
                  <div className="flex justify-between items-start gap-4">
                    <div className="space-y-1 flex-1">
                       <div className="text-sm font-medium">{evt.headline}</div>
                       <div className="text-xs text-muted-foreground">{evt.summary}</div>
                    </div>
                    <div className="flex flex-col items-end shrink-0 space-y-2">
                      <Badge variant="outline" className={`font-mono text-[10px] rounded-sm bg-transparent ${
                        evt.sentiment === 'positive' ? 'text-signal-positive border-signal-positive/30' : 
                        evt.sentiment === 'negative' ? 'text-signal-danger border-signal-danger/30' : 
                        'text-muted-foreground border-border'
                      }`}>
                        Vector: {evt.vector}
                      </Badge>
                      <div className="text-xs text-muted-foreground font-mono flex items-center gap-1">
                        <ExternalLink className="w-3 h-3" /> {evt.source}
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
