"use client";

import { motion } from "framer-motion";
import { MetricCard as MetricCardType } from "@/lib/types/executive";
import { 
  Building, DollarSign, Activity, 
  TrendingUp, ShieldAlert, BrainCircuit, Info
} from "lucide-react";
import dynamic from "next/dynamic";
import { useId, useMemo } from "react";

// Dynamically import Recharts to keep bundle small
const LineChart = dynamic(() => import("recharts").then(mod => mod.LineChart), { ssr: false });
const Line = dynamic(() => import("recharts").then(mod => mod.Line), { ssr: false });
const ResponsiveContainer = dynamic(() => import("recharts").then(mod => mod.ResponsiveContainer), { ssr: false });

const iconMap = {
  Building: Building,
  DollarSign: DollarSign,
  Activity: Activity,
  TrendingUp: TrendingUp,
  ShieldAlert: ShieldAlert,
  BrainCircuit: BrainCircuit,
};

interface MetricCardProps {
  data: MetricCardType;
}

export function MetricCard({ data }: MetricCardProps) {
  const Icon = iconMap[data.iconType] || Activity;
  const isPositive = data.trend > 0;
  const isNeutral = data.trend === 0;
  
  // Transform sparkline array to recharts format
  const chartData = useMemo(() => {
    return data.sparkline.map((val, i) => ({ value: val, index: i }));
  }, [data.sparkline]);

  const gradientId = useId();

  return (
    <motion.div 
      whileHover={{ y: -2 }}
      className="bg-surface-1 border border-border-default hover:border-border-strong rounded-md p-5 flex flex-col justify-between group transition-colors relative focus-within:ring-2 focus-within:ring-focus overflow-hidden"
    >
      <div className="flex justify-between items-start mb-4 relative z-10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-sm bg-surface-2 flex items-center justify-center text-primary group-hover:bg-surface-3 transition-colors">
            <Icon className="w-4 h-4" />
          </div>
          <span className="caption-sm text-secondary uppercase tracking-wider font-medium">
            {data.label}
          </span>
        </div>
        <button className="text-tertiary hover:text-primary transition-colors focus:outline-none" aria-label={`Info about ${data.label}`} title={`Calculated metric for ${data.label}`}>
          <Info className="w-4 h-4" />
        </button>
      </div>

      <div className="flex items-end justify-between relative z-10">
        <div>
          <div className="display-md text-primary font-mono tabular-nums leading-none tracking-tight">
            {data.value}
          </div>
          <div className="flex items-center gap-2 mt-2">
            <span className={`caption-md font-mono ${isPositive ? 'text-signal-positive' : isNeutral ? 'text-tertiary' : 'text-signal-danger'}`}>
              {isPositive ? '+' : ''}{data.trend}%
            </span>
            <span className="caption-sm text-tertiary">
              {data.trendLabel}
            </span>
          </div>
        </div>

        <div className="w-24 h-12 opacity-80 group-hover:opacity-20 transition-opacity">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <defs>
                <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="var(--color-fg-tertiary)" />
                  <stop offset="100%" stopColor={isPositive ? "var(--color-signal-positive)" : "var(--color-signal-danger)"} />
                </linearGradient>
              </defs>
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke={`url(#${gradientId})`} 
                strokeWidth={2}
                dot={false}
                isAnimationActive={true}
                animationDuration={1500}
                animationEasing="ease-out"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Progressive Disclosure: Why it matters */}
      <div className="absolute inset-0 bg-surface-2 p-5 flex flex-col justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none z-20 overflow-hidden">
        <h4 className="text-xs font-mono uppercase tracking-wider text-secondary mb-2">Why it matters</h4>
        <p className="text-sm text-primary leading-snug mb-3">
          {data.insight || `${data.label} trend indicates a shift in market dynamics.`}
        </p>
        <div className="flex flex-col gap-1.5 mt-auto">
          {data.impact && (
            <div className="text-xs text-secondary flex items-start gap-1">
              <span className="text-primary mt-0.5">•</span>
              <span>{data.impact}</span>
            </div>
          )}
          <div className="text-[10px] font-mono text-tertiary">
            Confidence: {data.confidence || 85}%
          </div>
        </div>
      </div>
    </motion.div>
  );
}
