"use client";

import { ExecutiveBrief } from "@/components/dashboard/ExecutiveBrief";
import { StrategicAlerts } from "@/components/dashboard/StrategicAlerts";
import { RecommendationBanner } from "@/components/dashboard/RecommendationBanner";
import { RecommendationCenter } from "@/components/dashboard/RecommendationCenter";
import { QuickActionCenter } from "@/components/dashboard/QuickActionCenter";
import { MetricGrid } from "@/components/dashboard/MetricGrid";
import { MarketSnapshotChart } from "@/components/dashboard/MarketSnapshot";
import { TopCompaniesTable } from "@/components/dashboard/TopCompaniesTable";
import { IntelligenceTimeline } from "@/components/dashboard/IntelligenceTimeline";
import { LiveTicker } from "@/components/dashboard/LiveTicker";
import { 
  useExecutiveBrief, 
  useTimeline, 
  useStrategicAlerts, 
  useRecommendations, 
  useTopCompanies, 
  useMarketSnapshot, 
  useMetrics 
} from "@/hooks/use-intelligence";
import { useWatchlistStore } from "@/stores/watchlist.store";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Star, EyeOff } from "lucide-react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const { data: timeline, isLoading: loadingTimeline, isError: errorTimeline } = useTimeline();
  const { data: executiveBrief, isLoading: loadingBrief, isError: errorBrief } = useExecutiveBrief();
  const { data: alerts, isLoading: loadingAlerts, isError: errorAlerts } = useStrategicAlerts();
  const { data: metrics, isLoading: loadingMetrics, isError: errorMetrics } = useMetrics();
  const { data: snapshot, isLoading: loadingSnapshot, isError: errorSnapshot } = useMarketSnapshot();
  const { data: companies, isLoading: loadingCompanies, isError: errorCompanies } = useTopCompanies();
  const { data: recommendations, isLoading: loadingRecs, isError: errorRecs } = useRecommendations();
  
  const watchedEntityIds = useWatchlistStore((state) => state.watchedEntityIds);
  const router = useRouter();

  // Derived state based on Watchlist
  const watchedCompanies = companies?.filter(c => watchedEntityIds.includes(c.name)) || [];
  const overnightDevelopments = timeline?.filter(t => watchedEntityIds.includes(t.companyName) || watchedEntityIds.length === 0).slice(0, 5) || [];

  return (
    <div className="flex flex-col gap-10 pb-16">
      
      {/* 0. Live Intelligence Ticker */}
      <div className="-mx-6 md:-mx-8 -mt-6 md:-mt-8 mb-2">
        {loadingTimeline ? (
          <div className="h-10 bg-slate-900 animate-pulse border-b border-white/10" />
        ) : (
          <LiveTicker events={timeline || []} />
        )}
      </div>

      <div className="flex items-center justify-between">
        <h1 className="sr-only">Executive Dashboard</h1>
        <QuickActionCenter />
      </div>

      {/* NEW: Watchlist Section */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-heading font-semibold flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500 fill-yellow-500/20" /> My Watchlist
          </h2>
        </div>
        {watchedCompanies.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {watchedCompanies.map(company => (
              <Card key={company.id} className="bg-card/40 backdrop-blur-sm border-border hover:bg-accent/50 cursor-pointer transition-colors" onClick={() => router.push(`/entities/${company.id}`)}>
                <CardHeader className="pb-2">
                  <CardTitle className="text-base flex justify-between items-start">
                    {company.name}
                    <span className={company.momentum > 70 ? "text-signal-positive text-sm" : "text-signal-danger text-sm"}>{company.momentum} Momentum</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xs text-muted-foreground">{company.recommendation || "Monitoring"}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="p-8 border border-dashed border-border rounded-xl text-center text-muted-foreground bg-muted/10">
            <EyeOff className="w-8 h-8 mx-auto mb-3 opacity-50" />
            <p>You aren't watching any entities yet.</p>
            <p className="text-xs mt-1">Search for a company and click the star to add it here.</p>
          </div>
        )}
      </section>

      {/* NEW: Overnight Developments */}
      <section>
        <div className="mb-4">
          <h2 className="text-xl font-heading font-semibold">Overnight Developments</h2>
          <p className="text-sm text-muted-foreground font-mono mt-1">Recent events from your watchlist and the broader market</p>
        </div>
        {loadingTimeline ? (
           <div className="h-64 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
        ) : (
           <IntelligenceTimeline events={overnightDevelopments} />
        )}
      </section>

      {/* 2. Strategic Banner (if multiple alerts suggest a macro trend) */}
      <section>
        <RecommendationBanner 
          message="Platform is running in Production mode, analyzing real-time data."
          evidenceCount={alerts?.length || 0}
          confidence={92}
          action="Review Active Alerts"
        />
      </section>

      {/* 3. Actionable Critical Alerts Layer */}
      <section>
        {loadingAlerts ? (
          <div className="h-32 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
        ) : alerts && alerts.length > 0 ? (
          <StrategicAlerts alerts={alerts} />
        ) : null}
      </section>

      {/* 4. Quantitative Layer (Milestone 3) */}
      <section>
        {loadingMetrics ? (
           <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
             {[1,2,3].map(i => <div key={i} className="h-32 bg-slate-900 animate-pulse rounded-xl border border-white/10" />)}
           </div>
        ) : metrics && metrics.length > 0 ? (
          <MetricGrid metrics={metrics} />
        ) : null}
      </section>

      <section>
        {loadingSnapshot ? (
          <div className="h-64 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
        ) : snapshot && snapshot.length > 0 ? (
          <MarketSnapshotChart data={snapshot} />
        ) : null}
      </section>

      {/* 5. Deep Intelligence Layer (Milestone 4) */}
      <section>
        {loadingRecs ? (
          <div className="h-64 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
        ) : recommendations && recommendations.length > 0 ? (
          <RecommendationCenter recommendations={recommendations} />
        ) : null}
      </section>

    </div>
  );
}
