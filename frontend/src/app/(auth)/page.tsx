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
  mockExecutiveBrief, 
  mockStrategicAlerts,
  mockRecommendations,
  mockMetrics,
  mockMarketSnapshots,
  mockTopCompanies,
  mockTimelineEvents
} from "@/lib/mock-data/executive";

export default function DashboardPage() {
  return (
    <div className="flex flex-col gap-10 pb-16">
      
      {/* 0. Live Intelligence Ticker */}
      <div className="-mx-6 md:-mx-8 -mt-6 md:-mt-8 mb-2">
        <LiveTicker events={mockTimelineEvents} />
      </div>

      <div className="flex items-center justify-between">
        <h1 className="sr-only">Executive Dashboard</h1>
        <QuickActionCenter />
      </div>

      {/* 1. Hero Narrative Layer */}
      <section>
        <ExecutiveBrief data={mockExecutiveBrief} />
      </section>

      {/* 2. Strategic Banner (if multiple alerts suggest a macro trend) */}
      <section>
        <RecommendationBanner 
          message="Three funding events indicate growing investor confidence in AI infrastructure."
          evidenceCount={3}
          confidence={92}
          action="Review Portfolio Exposure"
        />
      </section>

      {/* 3. Actionable Critical Alerts Layer */}
      <section>
        <StrategicAlerts alerts={mockStrategicAlerts} />
      </section>

      {/* 4. Quantitative Layer (Milestone 3) */}
      <section>
        <MetricGrid metrics={mockMetrics} />
      </section>

      <section>
        <MarketSnapshotChart data={mockMarketSnapshots} />
      </section>

      <section>
        <TopCompaniesTable companies={mockTopCompanies} />
      </section>

      {/* 5. Deep Intelligence Layer (Milestone 4) */}
      <section>
        <RecommendationCenter recommendations={mockRecommendations} />
      </section>

      <section>
        <IntelligenceTimeline events={mockTimelineEvents} />
      </section>

    </div>
  );
}
