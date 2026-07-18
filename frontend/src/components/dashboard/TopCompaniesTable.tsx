"use client";

import { motion } from "framer-motion";
import { CompanyMetric } from "@/lib/types/executive";
import { Info, TrendingUp, TrendingDown, Minus } from "lucide-react";
import dynamic from "next/dynamic";
import { useId } from "react";

const LineChart = dynamic(() => import("recharts").then(mod => mod.LineChart), { ssr: false });
const Line = dynamic(() => import("recharts").then(mod => mod.Line), { ssr: false });
const ResponsiveContainer = dynamic(() => import("recharts").then(mod => mod.ResponsiveContainer), { ssr: false });

interface TopCompaniesTableProps {
  companies: CompanyMetric[];
}

export function TopCompaniesTable({ companies }: TopCompaniesTableProps) {
  const getHeatmapColor = (score: number, inverse: boolean = false) => {
    // Inverse means higher is worse (e.g. Risk)
    const normalized = Math.max(0, Math.min(100, score));
    if (inverse) {
      if (normalized > 75) return "bg-signal-danger-subtle text-signal-danger";
      if (normalized > 50) return "bg-signal-warning-subtle text-signal-warning";
      return "bg-signal-positive-subtle text-signal-positive";
    } else {
      if (normalized > 85) return "bg-signal-positive-subtle text-signal-positive";
      if (normalized > 60) return "bg-signal-intelligence-subtle text-signal-intelligence";
      return "bg-surface-3 text-secondary";
    }
  };

  const TrendIcon = ({ direction }: { direction: CompanyMetric['trendDirection'] }) => {
    if (direction === 'up') return <TrendingUp className="w-4 h-4 text-signal-positive" />;
    if (direction === 'down') return <TrendingDown className="w-4 h-4 text-signal-danger" />;
    return <Minus className="w-4 h-4 text-tertiary" />;
  };

  const id = useId();

  return (
    <div className="flex flex-col gap-4">
      <header className="flex items-center justify-between">
        <h2 className="heading-md text-primary flex items-center gap-2">
          Company Momentum Matrix
          <span title="Companies scored by AI analysis of 30-day business events." className="text-tertiary cursor-help">
            <Info className="w-4 h-4" />
          </span>
        </h2>
      </header>

      <div className="bg-surface-1 border border-border-default rounded-md overflow-hidden overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr className="border-b border-border-default bg-surface-2 text-secondary caption-sm uppercase tracking-wider">
              <th className="py-3 px-4 font-medium">Company</th>
              <th className="py-3 px-4 font-medium text-right">Funding</th>
              <th className="py-3 px-4 font-medium text-center">Momentum</th>
              <th className="py-3 px-4 font-medium text-center">Growth</th>
              <th className="py-3 px-4 font-medium text-center">Risk</th>
              <th className="py-3 px-4 font-medium">Trend</th>
              <th className="py-3 px-4 font-medium">Action</th>
            </tr>
          </thead>
          <tbody>
            {companies.map((company, index) => (
              <motion.tr 
                key={company.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="border-b border-border-default hover:bg-surface-2 transition-colors group cursor-pointer"
              >
                <td className="py-4 px-4">
                  <span className="body-md text-primary font-medium">{company.name}</span>
                </td>
                <td className="py-4 px-4 text-right">
                  <span className="mono-md text-primary">
                    ${(company.fundingTotal / 1000000000).toFixed(1)}B
                  </span>
                </td>
                <td className="py-4 px-4 text-center">
                  <span className={`inline-block px-3 py-1 rounded-sm mono-sm font-bold ${getHeatmapColor(company.momentum)}`}>
                    {company.momentum}
                  </span>
                </td>
                <td className="py-4 px-4 text-center">
                  <span className={`inline-block px-3 py-1 rounded-sm mono-sm font-bold ${getHeatmapColor(company.growthScore)}`}>
                    {company.growthScore}
                  </span>
                </td>
                <td className="py-4 px-4 text-center">
                  <span className={`inline-block px-3 py-1 rounded-sm mono-sm font-bold ${getHeatmapColor(company.riskScore, true)}`}>
                    {company.riskScore}
                  </span>
                </td>
                <td className="py-4 px-4">
                  <div className="flex items-center gap-4">
                    <TrendIcon direction={company.trendDirection} />
                    <div className="w-16 h-6 opacity-60 group-hover:opacity-100 transition-opacity">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={company.sparklineData.map((v, i) => ({ value: v, index: i }))}>
                          <Line 
                            type="monotone" 
                            dataKey="value" 
                            stroke="var(--color-fg-secondary)" 
                            strokeWidth={1.5} 
                            dot={false}
                            isAnimationActive={false}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <span className="caption-sm text-primary uppercase font-bold tracking-widest border border-border-strong px-2 py-1 rounded-sm bg-base">
                    {company.recommendation}
                  </span>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
