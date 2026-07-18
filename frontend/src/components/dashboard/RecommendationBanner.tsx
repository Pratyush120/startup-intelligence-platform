"use client";

import { motion } from "framer-motion";
import { ArrowRight, Lightbulb } from "lucide-react";

interface RecommendationBannerProps {
  message: string;
  evidenceCount: number;
  confidence: number;
  action: string;
}

export function RecommendationBanner({
  message,
  evidenceCount,
  confidence,
  action
}: RecommendationBannerProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, ease: "easeOut", delay: 0.2 }}
      className="bg-surface-2 border border-border-default p-5 rounded-md flex flex-col sm:flex-row items-start sm:items-center gap-4 justify-between group hover:border-border-strong transition-colors"
    >
      <div className="flex items-start sm:items-center gap-4 flex-1">
        <div className="w-10 h-10 rounded-full bg-surface-3 flex items-center justify-center shrink-0 border border-border-default">
          <Lightbulb className="w-5 h-5 text-signal-intelligence" />
        </div>
        <div>
          <p className="body-md text-primary font-medium">{message}</p>
          <div className="flex items-center gap-3 mt-1">
            <span className="caption-sm text-secondary">
              Based on {evidenceCount} critical events
            </span>
            <span className="caption-sm text-tertiary">•</span>
            <span className="caption-sm font-mono text-secondary">
              Confidence: {confidence}%
            </span>
          </div>
        </div>
      </div>

      <button className="shrink-0 flex items-center gap-2 px-4 py-2 bg-primary text-inverted rounded-md caption-md hover:opacity-90 transition-opacity focus-visible:ring-2 focus-visible:ring-focus outline-none w-full sm:w-auto justify-center">
        {action}
        <ArrowRight className="w-4 h-4" />
      </button>
    </motion.div>
  );
}
