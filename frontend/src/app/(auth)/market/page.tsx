"use client";

import { useMarketSnapshot, useMetrics } from "@/hooks/use-intelligence";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, TrendingUp, TrendingDown, DollarSign, Activity, ShieldAlert } from "lucide-react";
import { InlineChart } from "@/components/ui/inline-chart";

export default function MarketPage() {
  const { data: metrics, isLoading: loadingMetrics } = useMetrics();
  const { data: snapshots, isLoading: loadingSnapshots } = useMarketSnapshot();

  const isLoading = loadingMetrics || loadingSnapshots;

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center min-h-[50vh]">
        <div className="flex flex-col items-center text-muted-foreground gap-4">
          <Loader2 className="w-8 h-8 animate-spin" />
          <p>Analyzing market intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 flex flex-col">
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h1 className="text-3xl font-heading font-semibold tracking-tight">Market Intelligence</h1>
          <p className="text-muted-foreground mt-2 font-mono text-sm">Ecosystem Health & Macro Trends</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {metrics?.map((metric) => {
          let Icon = Activity;
          if (metric.iconType === "DollarSign") Icon = DollarSign;
          if (metric.iconType === "ShieldAlert") Icon = ShieldAlert;
          
          const isPositiveTrend = metric.trend > 0;
          const TrendIcon = isPositiveTrend ? TrendingUp : TrendingDown;

          return (
            <Card key={metric.id} className="bg-card/40 backdrop-blur-sm border-border">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {metric.label}
                </CardTitle>
                <Icon className="w-4 h-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold tracking-tight">
                  {metric.iconType === "DollarSign" ? `$${(Number(metric.value) / 1000000).toFixed(1)}M` : metric.value}
                </div>
                <div className="flex items-center gap-2 mt-2">
                  <div className={`flex items-center text-xs font-mono ${isPositiveTrend ? 'text-signal-positive' : 'text-signal-danger'}`}>
                    <TrendIcon className="w-3 h-3 mr-1" />
                    {Math.abs(metric.trend)}%
                  </div>
                  <span className="text-xs text-muted-foreground">{metric.trendLabel}</span>
                </div>
                <div className="mt-4 h-[40px] opacity-70">
                  <InlineChart 
                    data={metric.sparkline} 
                    color={isPositiveTrend ? '#059669' : '#DC2626'} 
                  />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Card className="flex-1 min-h-[400px] border-border bg-card/40 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-lg font-medium">Market Health Timeline</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center h-full">
           <div className="text-center text-muted-foreground">
             <p className="font-mono text-sm mb-4">Historical Chart Data</p>
             <p className="text-xs max-w-sm mx-auto">
                Detailed visualizations are currently rendering. We have mapped {snapshots?.length || 0} historical data points from the pipeline.
             </p>
           </div>
        </CardContent>
      </Card>
    </div>
  );
}
