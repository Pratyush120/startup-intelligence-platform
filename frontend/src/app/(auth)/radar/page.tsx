"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { RadarGraph } from "@/components/ui/radar-graph"
import { Compass, Filter } from "lucide-react"
import { useTrends } from "@/hooks/use-intelligence"
import { MacroTrend } from "@/lib/types"

export default function RadarPage() {
  const { data: trends, isLoading, isError } = useTrends();
  
  // Mock Plotly Data for the Topology Graph (Keep standard graph layout for now)
  const graphData = [
    {
      x: [1, 2, 3, 4, 2, 3],
      y: [2, 1, 3, 2, 4, 1],
      mode: 'markers+lines',
      type: 'scatter',
      marker: { 
        size: [20, 40, 15, 30, 25, 35],
        color: ['#3730A3', '#065F46', '#92400E', '#3730A3', '#991B1B', '#065F46'],
        opacity: 0.8 
      },
      line: {
        color: '#27272A',
        width: 1
      },
      text: ['Entity A', 'Trend X', 'Entity C', 'Entity D', 'Trend Y', 'Trend Z'],
      hoverinfo: 'text'
    }
  ];

  const graphLayout = {
    xaxis: { showgrid: false, zeroline: false, showticklabels: false },
    yaxis: { showgrid: false, zeroline: false, showticklabels: false },
    hovermode: 'closest'
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 flex flex-col h-[calc(100vh-4rem)]">
      {/* Header */}
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h1 className="text-3xl font-heading font-semibold tracking-tight">Market Radar</h1>
          <p className="text-muted-foreground mt-2 font-mono text-sm">Topology Mapping & Trend Velocity</p>
        </div>
        <div className="flex gap-2">
          <Badge variant="outline" className="px-3 py-1 cursor-pointer hover:bg-accent flex items-center gap-2 rounded-sm border-border">
            <Filter className="w-3 h-3" /> Sector: Supply Chain AI
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 flex-1 min-h-0">
        
        {/* Left Sidebar (3 cols) */}
        <div className="xl:col-span-3 flex flex-col gap-4 overflow-y-auto pr-2">
          <h2 className="text-sm font-mono text-muted-foreground uppercase tracking-wider flex items-center gap-2">
            <Compass className="w-4 h-4" /> Trend Velocity
          </h2>
          
          <div className="space-y-3">
            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map(i => (
                  <div key={i} className="h-20 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
                ))}
              </div>
            ) : isError ? (
               <div className="text-red-400 text-sm">Failed to load trends</div>
            ) : trends?.map((trend: MacroTrend) => (
              <button key={trend.id} className="w-full text-left group">
                <Card className="border-border bg-card/40 hover:bg-accent/50 transition-colors group-focus:border-signal-intelligence">
                  <CardContent className="p-4 flex items-center justify-between">
                    <div>
                      <div className="font-medium text-sm">{trend.name}</div>
                      <div className="text-xs text-muted-foreground mt-1">{trend.sector}</div>
                    </div>
                    <div className={trend.velocity > 0 ? "text-signal-positive" : "text-signal-danger"}>
                      <span className="text-xs font-mono font-medium">{trend.velocity > 0 ? "+" : ""}{trend.velocity}%</span>
                    </div>
                  </CardContent>
                </Card>
              </button>
            ))}
          </div>
        </div>

        {/* Right Main Area (9 cols) */}
        <div className="xl:col-span-9 flex flex-col gap-8 min-h-0">
          
          {/* Topology Map */}
          <Card className="flex-1 min-h-0 flex flex-col overflow-hidden">
            <CardHeader className="pb-0 shrink-0">
              <CardTitle className="text-sm font-mono text-muted-foreground uppercase">Knowledge Graph</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 p-0 relative">
              <div className="absolute inset-0">
                 <RadarGraph data={graphData} layout={graphLayout} />
              </div>
            </CardContent>
          </Card>

          {/* Data Grid */}
          <Card className="shrink-0 max-h-[300px] flex flex-col">
             <CardHeader className="py-4 border-b border-border bg-muted/20 shrink-0">
              <CardTitle className="text-sm font-medium">Emerging Technologies Data Grid</CardTitle>
            </CardHeader>
            <CardContent className="p-0 overflow-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs font-mono text-muted-foreground bg-muted/20 sticky top-0 border-b border-border">
                  <tr>
                    <th className="px-6 py-3 font-medium">Technology Focus</th>
                    <th className="px-6 py-3 font-medium text-right">Velocity</th>
                    <th className="px-6 py-3 font-medium">Leading Entity</th>
                    <th className="px-6 py-3 font-medium">Market Sentiment</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {isLoading ? (
                    <tr>
                      <td colSpan={4} className="p-4 text-center text-muted-foreground">Loading...</td>
                    </tr>
                  ) : trends?.map((trend: MacroTrend) => (
                    <tr key={trend.id} className="hover:bg-muted/30 transition-colors">
                      <td className="px-6 py-3 font-medium">{trend.name}</td>
                      <td className="px-6 py-3 text-right font-mono text-muted-foreground">
                         <span className={trend.velocity > 0 ? "text-signal-positive" : "text-signal-danger"}>
                           {trend.velocity > 0 ? "+" : ""}{trend.velocity}%
                         </span>
                      </td>
                      <td className="px-6 py-3 text-muted-foreground">Nexus Robotics</td>
                      <td className="px-6 py-3">
                         <Badge variant="outline" className="font-mono bg-transparent">Neutral</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>

        </div>
      </div>
    </div>
  )
}

