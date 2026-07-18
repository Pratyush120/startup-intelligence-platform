"use client"

import dynamic from 'next/dynamic'
import { Skeleton } from '@/components/ui/skeleton'

const Plot = dynamic(() => import('react-plotly.js'), { 
  ssr: false,
  loading: () => <Skeleton className="w-[120px] h-[40px] bg-muted/50 rounded-sm" />
})

interface InlineChartProps {
  data: number[];
  color?: string;
  isThreat?: boolean;
}

export function InlineChart({ data, color = '#71717A', isThreat = false }: InlineChartProps) {
  
  const plotData = [
    {
      y: data,
      type: 'scatter',
      mode: 'lines',
      fill: 'tozeroy',
      line: {
        color: isThreat ? '#7F1D1D' : color, // Deep Crimson or Neutral
        width: 1.5,
      },
      fillcolor: isThreat ? 'rgba(127, 29, 29, 0.1)' : 'rgba(113, 113, 122, 0.1)',
      hoverinfo: 'none'
    }
  ];

  const layout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    margin: { t: 0, r: 0, b: 0, l: 0 },
    xaxis: { showgrid: false, zeroline: false, showticklabels: false, fixedrange: true },
    yaxis: { showgrid: false, zeroline: false, showticklabels: false, fixedrange: true },
    showlegend: false,
    hovermode: false
  };

  return (
    <div className="w-[120px] h-[40px] inline-block align-middle ml-4">
      <Plot
        data={plotData as any}
        layout={layout as any}
        config={{ displayModeBar: false, responsive: true }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  )
}
