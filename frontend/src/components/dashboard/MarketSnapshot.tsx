"use client";

import { useMemo } from "react";
import dynamic from "next/dynamic";
import { MarketSnapshot } from "@/lib/types/executive";
import { Info } from "lucide-react";
import { motion } from "framer-motion";

const AreaChart = dynamic(() => import("recharts").then(mod => mod.AreaChart), { ssr: false, loading: () => <div className="w-full h-full animate-pulse bg-surface-2 rounded-md" /> });
const Area = dynamic(() => import("recharts").then(mod => mod.Area), { ssr: false });
const XAxis = dynamic(() => import("recharts").then(mod => mod.XAxis), { ssr: false });
const YAxis = dynamic(() => import("recharts").then(mod => mod.YAxis), { ssr: false });
const Tooltip = dynamic(() => import("recharts").then(mod => mod.Tooltip), { ssr: false });
const ResponsiveContainer = dynamic(() => import("recharts").then(mod => mod.ResponsiveContainer), { ssr: false });

interface MarketSnapshotChartProps {
  data: MarketSnapshot[];
}

export function MarketSnapshotChart({ data }: MarketSnapshotChartProps) {
  // Memoize data to prevent unnecessary re-renders
  const chartData = useMemo(() => {
    return data.map(d => ({
      ...d,
      formattedDate: new Date(d.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
    }));
  }, [data]);

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      className="bg-surface-1 border border-border-default rounded-md p-6 flex flex-col gap-6"
    >
      <header className="flex items-center justify-between">
        <div>
          <h2 className="heading-md text-primary flex items-center gap-2">
            Market Event Volume
            <span title="Aggregate volume of funding, hiring, and layoff events over 30 days." className="text-tertiary cursor-help">
              <Info className="w-4 h-4" />
            </span>
          </h2>
          <p className="caption-sm text-secondary mt-1">Total business events extracted per day</p>
        </div>
      </header>

      <div className="w-full h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorFunding" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-signal-positive)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="var(--color-signal-positive)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorHiring" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-signal-intelligence)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="var(--color-signal-intelligence)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorLayoffs" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-signal-danger)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="var(--color-signal-danger)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis 
              dataKey="formattedDate" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: 'var(--color-fg-secondary)', fontSize: 12 }} 
              minTickGap={30}
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: 'var(--color-fg-secondary)', fontSize: 12 }} 
            />
            <Tooltip 
              contentStyle={{ backgroundColor: 'var(--color-bg-surface-2)', border: '1px solid var(--color-border-default)', borderRadius: '6px', color: 'var(--color-fg-primary)' }}
              itemStyle={{ color: 'var(--color-fg-primary)' }}
            />
            <Area 
              type="monotone" 
              dataKey="fundingAmount" 
              stackId="1" 
              stroke="var(--color-signal-positive)" 
              fill="url(#colorFunding)" 
              isAnimationActive={true}
              animationDuration={1500}
            />
            <Area 
              type="monotone" 
              dataKey="hiringEvents" 
              stackId="1" 
              stroke="var(--color-signal-intelligence)" 
              fill="url(#colorHiring)" 
              isAnimationActive={true}
              animationDuration={1500}
            />
            <Area 
              type="monotone" 
              dataKey="layoffEvents" 
              stackId="1" 
              stroke="var(--color-signal-danger)" 
              fill="url(#colorLayoffs)" 
              isAnimationActive={true}
              animationDuration={1500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
