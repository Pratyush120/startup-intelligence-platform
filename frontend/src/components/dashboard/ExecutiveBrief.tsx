"use client";

import { motion } from "framer-motion";
import { ExecutiveBrief as ExecutiveBriefType } from "@/lib/types/executive";

interface ExecutiveBriefProps {
  data: ExecutiveBriefType;
}

export function ExecutiveBrief({ data }: ExecutiveBriefProps) {
  const {
    strategicSummary,
    primaryRecommendation,
    marketHealthScore,
    investmentClimate,
    growthOutlook,
    riskLevel,
    confidenceScore,
  } = data;

  return (
    <motion.article 
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="bg-surface-1 border border-border-default rounded-md p-6 md:p-8 flex flex-col gap-6"
    >
      <header>
        <h1 className="heading-xl text-primary mb-2">Today's Executive Brief</h1>
        <p className="body-lg text-secondary leading-relaxed">
          {strategicSummary}
        </p>
      </header>

      {/* Narrative First Recommendation */}
      <div className="bg-signal-intelligence-subtle border border-signal-intelligence/20 p-5 rounded-md flex gap-4 items-start">
        <div className="w-1.5 h-10 bg-signal-intelligence rounded-full shrink-0" />
        <div>
          <h2 className="heading-sm text-primary mb-1">Primary Recommendation</h2>
          <p className="body-md text-primary font-medium">{primaryRecommendation}</p>
        </div>
      </div>

      {/* Supporting Data Tags */}
      <div className="flex flex-wrap gap-4 mt-2">
        <div className="flex flex-col gap-1">
          <span className="caption-sm text-tertiary uppercase tracking-wider">Market Health</span>
          <span className="body-md font-medium text-primary">{marketHealthScore}/100</span>
        </div>
        <div className="w-px bg-border-default h-10 hidden sm:block" />
        
        <div className="flex flex-col gap-1">
          <span className="caption-sm text-tertiary uppercase tracking-wider">Climate</span>
          <span className="body-md font-medium text-primary">{investmentClimate}</span>
        </div>
        <div className="w-px bg-border-default h-10 hidden sm:block" />
        
        <div className="flex flex-col gap-1">
          <span className="caption-sm text-tertiary uppercase tracking-wider">Growth</span>
          <span className="body-md font-medium text-primary">{growthOutlook}</span>
        </div>
        <div className="w-px bg-border-default h-10 hidden sm:block" />
        
        <div className="flex flex-col gap-1">
          <span className="caption-sm text-tertiary uppercase tracking-wider">Risk</span>
          <span className="body-md font-medium text-primary">{riskLevel}</span>
        </div>
        <div className="w-px bg-border-default h-10 hidden sm:block" />
        
        <div className="flex flex-col gap-1">
          <span className="caption-sm text-tertiary uppercase tracking-wider">Confidence</span>
          <span className="body-md font-medium text-primary">{confidenceScore}%</span>
        </div>
      </div>
    </motion.article>
  );
}
