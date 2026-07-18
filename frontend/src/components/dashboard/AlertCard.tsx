"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { StrategicAlert } from "@/lib/types/executive";
import { ChevronDown, AlertTriangle, AlertCircle, Info } from "lucide-react";

interface AlertCardProps {
  alert: StrategicAlert;
}

export function AlertCard({ alert }: AlertCardProps) {
  const [expanded, setExpanded] = useState(false);

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
    <motion.button
      layout
      onClick={() => setExpanded(!expanded)}
      className="w-full text-left group border border-border-default bg-base rounded-md p-4 md:p-5 hover:border-border-strong transition-colors focus-visible:ring-2 focus-visible:ring-focus outline-none flex flex-col gap-3"
      aria-expanded={expanded}
    >
      <div className="flex items-start justify-between w-full gap-4">
        <div className="flex items-start gap-3 flex-1">
          <div className="mt-0.5 shrink-0">
            <PriorityIcon priority={alert.priority} />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className="caption-sm text-primary font-medium tracking-wide uppercase px-2 py-0.5 rounded-sm bg-surface-2">
                {alert.companyName}
              </span>
              <span className="caption-sm text-secondary">
                {alert.category}
              </span>
              <span className="caption-sm text-tertiary hidden sm:inline-block">
                • {new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            <h3 className="heading-sm text-primary leading-snug pr-4">{alert.title}</h3>
          </div>
        </div>
        
        <motion.div 
          animate={{ rotate: expanded ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="shrink-0 text-tertiary group-hover:text-primary transition-colors"
        >
          <ChevronDown className="w-5 h-5" />
        </motion.div>
      </div>

      <AnimatePresence initial={false}>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: "easeInOut" }}
            className="overflow-hidden w-full"
          >
            <div className="pt-2 pb-1 border-t border-border-default mt-2">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                <div>
                  <span className="caption-sm text-tertiary uppercase tracking-wider block mb-1">Business Impact</span>
                  <p className="body-sm text-secondary">{alert.impact}</p>
                </div>
                <div>
                  <span className="caption-sm text-tertiary uppercase tracking-wider block mb-1">Suggested Action</span>
                  <p className="body-sm text-primary font-medium">{alert.recommendation}</p>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between text-xs">
                <span className="text-secondary font-mono">Confidence: {alert.confidence}%</span>
                <span className={`px-2 py-1 rounded-sm ${getPriorityColor(alert.priority)} font-mono uppercase font-bold tracking-wider`}>
                  {alert.priority}
                </span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.button>
  );
}
