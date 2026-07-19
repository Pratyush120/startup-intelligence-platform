"use client";

import { StrategicAlert } from "@/lib/types/executive";
import { AlertTriangle, AlertCircle, Info } from "lucide-react";

interface AlertCardProps {
  alert: StrategicAlert;
}

export function AlertCard({ alert }: AlertCardProps) {
  const getPriorityColor = (priority: StrategicAlert["priority"]) => {
    switch (priority) {
      case "Critical": return "bg-signal-danger text-signal-danger-subtle";
      case "High": return "bg-signal-warning text-signal-warning-subtle";
      case "Medium": return "bg-signal-intelligence text-signal-intelligence-subtle";
      case "Low": return "bg-surface-3 text-secondary";
      default: return "bg-surface-3 text-secondary";
    }
  };

  const PriorityIcon = ({ priority }: { priority: StrategicAlert["priority"] }) => {
    switch (priority) {
      case "Critical": return <AlertTriangle className="w-4 h-4 text-signal-danger" />;
      case "High": return <AlertCircle className="w-4 h-4 text-signal-warning" />;
      case "Medium": return <Info className="w-4 h-4 text-signal-intelligence" />;
      case "Low": return <Info className="w-4 h-4 text-tertiary" />;
      default: return null;
    }
  };

  return (
    <div
      className="w-full text-left group border border-border bg-card/40 backdrop-blur-sm rounded-xl p-5 hover:border-primary/50 transition-colors flex flex-col gap-4 shadow-sm"
    >
      <div className="flex items-start justify-between w-full gap-4">
        <div className="flex items-start gap-3 flex-1">
          <div className="mt-1 shrink-0 bg-background rounded-full p-1.5 border border-border">
            <PriorityIcon priority={alert.priority} />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-2 flex-wrap">
              <span className="text-xs font-bold tracking-wide uppercase px-2 py-0.5 rounded-full bg-muted/50 border border-border text-foreground">
                {alert.companyName}
              </span>
              <span className="text-xs text-muted-foreground uppercase font-mono tracking-wider">
                {alert.category}
              </span>
              <span className="text-xs text-muted-foreground font-mono hidden sm:inline-block">
                • {new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            <h3 className="text-lg font-semibold text-foreground leading-snug pr-4">{alert.title}</h3>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-2">
        <div className="p-4 bg-muted/20 border border-border/50 rounded-lg">
          <h4 className="text-xs font-mono text-muted-foreground uppercase tracking-wider mb-2">Why this matters</h4>
          <p className="text-sm text-foreground leading-relaxed">{alert.impact}</p>
        </div>
        <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
          <h4 className="text-xs font-mono text-primary uppercase tracking-wider mb-2 flex items-center gap-2">
            Suggested Action
          </h4>
          <p className="text-sm text-foreground font-medium">{alert.recommendation}</p>
        </div>
      </div>
      
      <div className="flex items-center justify-between text-xs mt-2 border-t border-border pt-4">
        <span className="text-muted-foreground font-mono">AI Confidence: {alert.confidence}%</span>
        <span className={`px-2 py-1 rounded-sm ${getPriorityColor(alert.priority)} font-mono uppercase font-bold tracking-wider text-[10px]`}>
          Priority: {alert.priority}
        </span>
      </div>
    </div>
  );
}
