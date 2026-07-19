"use client"

import dynamic from 'next/dynamic'
import { useTheme } from 'next-themes'
import { Skeleton } from '@/components/ui/skeleton'

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { 
  ssr: false,
  loading: () => <Skeleton className="w-full h-full bg-muted/50" />
})

// Plotly's own data/layout props accept unknown[] and unknown per react-plotly.js typings.
// We use Record<string, unknown> to stay type-safe without depending on @types/plotly.js internals.
interface RadarGraphProps {
  data: Record<string, unknown>[];
  layout?: Record<string, unknown>;
}

export function RadarGraph({ data, layout }: RadarGraphProps) {
  const { resolvedTheme } = useTheme();
  
  const isDark = resolvedTheme === 'dark';
  
  const baseLayout: Record<string, unknown> = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: {
      family: 'var(--font-sans)',
      color: isDark ? '#A1A1AA' : '#71717A',
    },
    margin: { t: 20, r: 20, b: 20, l: 20 },
    ...layout
  };

  return (
    <div className="w-full h-full min-h-[400px]">
      <Plot
        data={data}
        layout={baseLayout}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false, responsive: true }}
      />
    </div>
  )
}
