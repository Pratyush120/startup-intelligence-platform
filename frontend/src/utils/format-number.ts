export function formatScore(value: number): string {
  return value.toFixed(0);
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(0)}%`;
}

export function formatDelta(value: number): string {
  const prefix = value > 0 ? "↑" : value < 0 ? "↓" : "";
  return `${prefix} ${Math.abs(value).toFixed(1)}`;
}

export function formatCurrency(value: number): string {
  if (value >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(1)}B`;
  if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(0)}M`;
  if (value >= 1_000) return `$${(value / 1_000).toFixed(0)}K`;
  return `$${value}`;
}
