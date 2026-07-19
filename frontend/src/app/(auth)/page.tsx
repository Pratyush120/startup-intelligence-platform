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
    <div className="flex flex-col gap-12 pb-16 pt-4">
      
      {/* 0. Live Intelligence Ticker */}
      <div className="-mx-6 md:-mx-8 -mt-10 md:-mt-12 mb-2">
        {loadingTimeline ? (
          <div className="h-10 bg-surface-2 animate-pulse border-b border-border-default" />
        ) : (
          <LiveTicker events={timeline || []} />
        )}
      </div>

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-primary">Good Morning.</h1>
          <p className="text-secondary mt-2">Here is your strategic intelligence briefing for today.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        <div className="xl:col-span-2 flex flex-col gap-10">
          {/* 1. Hero Narrative Layer (Executive Brief) */}
          <section>
            {loadingBrief ? (
              <div className="h-48 bg-surface-2 animate-pulse rounded-xl border border-border-default" />
            ) : errorBrief ? (
              <div className="p-4 border border-red-500/50 bg-red-500/10 rounded-xl text-red-200">Failed to load Executive Brief.</div>
            ) : executiveBrief ? (
              <ExecutiveBrief data={executiveBrief} />
            ) : (
              <div className="p-4 border border-border-default rounded-xl text-secondary">We are currently gathering intelligence.</div>
            )}
          </section>

          {/* 2. Actionable Critical Alerts Layer */}
          <section>
            <h2 className="text-xl font-semibold text-primary mb-4">High Priority Events</h2>
            {loadingAlerts ? (
              <div className="h-32 bg-surface-2 animate-pulse rounded-xl border border-border-default" />
            ) : alerts && alerts.length > 0 ? (
              <StrategicAlerts alerts={alerts} />
            ) : (
               <div className="p-4 border border-border-default rounded-xl text-secondary text-sm">No high priority alerts overnight.</div>
            )}
          </section>
          
          {/* 3. Deep Intelligence Layer (Recommendations) */}
          <section>
            <h2 className="text-xl font-semibold text-primary mb-4">AI Recommendations</h2>
            {loadingRecs ? (
              <div className="h-64 bg-surface-2 animate-pulse rounded-xl border border-border-default" />
            ) : recommendations && recommendations.length > 0 ? (
              <RecommendationCenter recommendations={recommendations} />
            ) : null}
          </section>
          
          {/* 4. Companies Requiring Attention */}
          <section>
             <h2 className="text-xl font-semibold text-primary mb-4">Companies Requiring Attention</h2>
            {loadingCompanies ? (
              <div className="h-64 bg-surface-2 animate-pulse rounded-xl border border-border-default" />
            ) : companies && companies.length > 0 ? (
              <TopCompaniesTable companies={companies.slice(0,5)} />
            ) : null}
          </section>
        </div>

        <div className="flex flex-col gap-10">
          {/* 5. Quantitative Layer (Market Signals) */}
          <section>
            <h2 className="text-lg font-semibold text-primary mb-4">Market Signals</h2>
            {loadingMetrics ? (
               <div className="flex flex-col gap-4">
                 {[1,2,3,4].map(i => <div key={i} className="h-24 bg-surface-2 animate-pulse rounded-xl border border-border-default" />)}
               </div>
            ) : metrics && metrics.length > 0 ? (
              <div className="flex flex-col gap-4">
                <MetricGrid metrics={metrics} />
              </div>
            ) : null}
          </section>

          {/* Quick Access */}
          <section>
            <h2 className="text-lg font-semibold text-primary mb-4">Quick Access</h2>
            <QuickActionCenter />
          </section>
        </div>
      </div>
    </div>
  );
}
