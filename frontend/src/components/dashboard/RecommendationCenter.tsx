"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Recommendation } from "@/lib/types/executive";
import { BrainCircuit, ChevronDown, BookOpen } from "lucide-react";
import { Drawer } from "@/components/ui/drawer";
import { EvidencePanel } from "./EvidencePanel";

interface RecommendationCenterProps {
  recommendations: Recommendation[];
}

export function RecommendationCenter({ recommendations }: RecommendationCenterProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [drawerData, setDrawerData] = useState<Recommendation | null>(null);

  if (!recommendations.length) {
    return (
      <div className="p-8 border border-dashed border-border-default rounded-md text-center bg-surface-1">
        <BrainCircuit className="w-8 h-8 text-tertiary mx-auto mb-3" />
        <h3 className="heading-sm text-primary mb-1">No AI Recommendations</h3>
        <p className="caption-sm text-secondary">The intelligence engine has not detected strategic anomalies today.</p>
      </div>
    );
  }

  return (
    <>
      <section className="flex flex-col gap-4">
        <header className="flex items-center justify-between">
          <h2 className="heading-md text-primary flex items-center gap-2">
            AI Recommendation Center
          </h2>
        </header>

        <div className="flex flex-col gap-4">
          {recommendations.map((rec) => {
            const isExpanded = expandedId === rec.id;
            return (
              <motion.div 
                key={rec.id}
                layout
                className="bg-base border border-border-default rounded-md hover:border-border-strong transition-colors overflow-hidden focus-within:ring-2 focus-within:ring-focus"
              >
                <div 
                  className="p-5 cursor-pointer flex flex-col gap-3"
                  onClick={() => setExpandedId(isExpanded ? null : rec.id)}
                  role="button"
                  aria-expanded={isExpanded}
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      setExpandedId(isExpanded ? null : rec.id);
                    }
                  }}
                >
                  <div className="flex justify-between items-start gap-4">
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5">
                        <BrainCircuit className="w-5 h-5 text-signal-intelligence" />
                      </div>
                      <div>
                        <div className="flex items-center gap-3 mb-1">
                          <span className={`caption-sm font-bold uppercase tracking-wider px-2 py-0.5 rounded-sm ${
                            rec.priority === 'High' ? 'bg-signal-warning text-signal-warning-subtle' : 'bg-surface-2 text-secondary'
                          }`}>
                            {rec.priority} Priority
                          </span>
                          <span className="caption-sm text-tertiary font-mono">
                            {rec.confidence}% Confidence
                          </span>
                        </div>
                        <h3 className="heading-sm text-primary">{rec.title}</h3>
                      </div>
                    </div>
                    <motion.div 
                      animate={{ rotate: isExpanded ? 180 : 0 }}
                      className="text-tertiary"
                    >
                      <ChevronDown className="w-5 h-5" />
                    </motion.div>
                  </div>
                </div>

                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3, ease: "easeInOut" }}
                    >
                      <div className="p-5 pt-0 border-t border-border-default bg-surface-1">
                        <div className="mt-4 flex flex-col gap-4">
                          <div>
                            <span className="caption-sm text-tertiary uppercase tracking-wider mb-1 block">Strategic Impact</span>
                            <p className="body-sm text-primary font-medium">{rec.strategicImpact}</p>
                          </div>
                          <div>
                            <span className="caption-sm text-tertiary uppercase tracking-wider mb-1 block">Business Reason</span>
                            <p className="body-sm text-secondary">{rec.reason}</p>
                          </div>
                          
                          <div className="mt-2 flex gap-3">
                            <button className="flex-1 bg-primary text-inverted py-2 rounded-md font-medium hover:opacity-90 transition-opacity">
                              {rec.suggestedAction}
                            </button>
                            <button 
                              onClick={(e) => { e.stopPropagation(); setDrawerData(rec); }}
                              className="px-4 py-2 border border-border-strong text-primary rounded-md font-medium hover:bg-surface-2 transition-colors flex items-center gap-2 justify-center"
                            >
                              <BookOpen className="w-4 h-4" />
                              View Evidence
                            </button>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>
      </section>

      <Drawer 
        open={!!drawerData} 
        onClose={() => setDrawerData(null)}
      >
        {drawerData && <EvidencePanel recommendation={drawerData} />}
      </Drawer>
    </>
  );
}
