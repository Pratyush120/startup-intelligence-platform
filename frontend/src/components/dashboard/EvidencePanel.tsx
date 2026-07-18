"use client";

import { motion } from "framer-motion";
import { Recommendation } from "@/lib/types/executive";
import { CheckCircle2, TrendingUp, AlertTriangle, ShieldCheck } from "lucide-react";

interface EvidencePanelProps {
  recommendation: Recommendation;
}

export function EvidencePanel({ recommendation }: EvidencePanelProps) {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col gap-6"
    >
      <div className="flex items-center justify-between p-4 bg-surface-2 border border-border-default rounded-md">
        <div className="flex flex-col gap-1">
          <span className="caption-sm text-tertiary uppercase tracking-wider">Evidence Score</span>
          <span className="heading-lg text-primary tabular-nums tracking-tight">
            {recommendation.evidenceScore}/100
          </span>
        </div>
        <ShieldCheck className="w-8 h-8 text-signal-intelligence opacity-80" />
      </div>

      <section>
        <h4 className="caption-sm text-tertiary uppercase tracking-wider mb-3">Supporting Evidence</h4>
        <ul className="space-y-3">
          {recommendation.evidence.map((ev, i) => (
            <li key={i} className="flex items-start gap-3">
              <CheckCircle2 className="w-4 h-4 text-signal-positive shrink-0 mt-0.5" />
              <span className="body-sm text-secondary">{ev}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="grid grid-cols-2 gap-4">
        <div className="p-4 border border-border-default rounded-md bg-surface-1">
          <div className="flex items-center gap-2 mb-2 text-signal-positive">
            <TrendingUp className="w-4 h-4" />
            <span className="caption-sm uppercase font-bold tracking-wider">Opportunity</span>
          </div>
          <p className="body-sm text-primary font-medium">{recommendation.estimatedOpportunity}</p>
        </div>
        
        <div className="p-4 border border-border-default rounded-md bg-surface-1">
          <div className="flex items-center gap-2 mb-2 text-signal-warning">
            <AlertTriangle className="w-4 h-4" />
            <span className="caption-sm uppercase font-bold tracking-wider">Risk Profile</span>
          </div>
          <p className="body-sm text-primary font-medium">{recommendation.estimatedRisk}</p>
        </div>
      </section>

      <section>
        <h4 className="caption-sm text-tertiary uppercase tracking-wider mb-2">Affected Ecosystem</h4>
        <div className="flex flex-wrap gap-2">
          {recommendation.relatedCompanies.map(company => (
            <span key={company} className="caption-sm text-primary bg-surface-2 border border-border-default px-2 py-1 rounded-sm">
              {company}
            </span>
          ))}
        </div>
      </section>

    </motion.div>
  );
}
