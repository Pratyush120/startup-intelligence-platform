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

export default function DashboardPage() {
  const { data: timeline, isLoading: loadingTimeline, isError: errorTimeline } = useTimeline();
  const { data: executiveBrief, isLoading: loadingBrief, isError: errorBrief } = useExecutiveBrief();
  const { data: alerts, isLoading: loadingAlerts, isError: errorAlerts } = useStrategicAlerts();
  const { data: metrics, isLoading: loadingMetrics, isError: errorMetrics } = useMetrics();
  const { data: snapshot, isLoading: loadingSnapshot, isError: errorSnapshot } = useMarketSnapshot();
  const { data: companies, isLoading: loadingCompanies, isError: errorCompanies } = useTopCompanies();
  const { data: recommendations, isLoading: loadingRecs, isError: errorRecs } = useRecommendations();

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

      {/* 1. Hero Narrative Layer */}
      <section>
        {loadingBrief ? (
          <div className="h-48 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
        ) : errorBrief ? (
          <div className="p-4 border border-red-500/50 bg-red-500/10 rounded-xl text-red-200">Failed to load Executive Brief.</div>
        ) : executiveBrief ? (
          <ExecutiveBrief data={executiveBrief} />
        ) : (
          <div className="p-4 border border-white/10 rounded-xl text-slate-400">No executive brief available.</div>
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

      <section>
        {loadingCompanies ? (
          <div className="h-64 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
        ) : companies && companies.length > 0 ? (
          <TopCompaniesTable companies={companies} />
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

      <section>
        {loadingTimeline ? (
          <div className="h-64 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
        ) : timeline && timeline.length > 0 ? (
          <IntelligenceTimeline events={timeline} />
        ) : null}
      </section>

    </div>
  );
}
