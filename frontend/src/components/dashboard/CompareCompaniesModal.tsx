"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, GitCompare, Loader2, Building2, TrendingUp, AlertTriangle, Activity } from "lucide-react";
import { useTopCompanies } from "@/hooks/use-intelligence";
import { CompanyMetric } from "@/lib/types/executive";

interface CompareCompaniesModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CompareCompaniesModal({ isOpen, onClose }: CompareCompaniesModalProps) {
  const { data: companies, isLoading } = useTopCompanies();
  const [selectedCompany1, setSelectedCompany1] = useState<string>("");
  const [selectedCompany2, setSelectedCompany2] = useState<string>("");

  if (!isOpen) return null;

  const company1 = companies?.find(c => c.name === selectedCompany1) || null;
  const company2 = companies?.find(c => c.name === selectedCompany2) || null;

  const renderMetric = (label: string, value1: any, value2: any, Icon: React.ElementType, higherIsBetter = true) => {
    let color1 = "text-primary";
    let color2 = "text-primary";
    
    if (value1 !== undefined && value2 !== undefined) {
      if (value1 > value2) {
        color1 = higherIsBetter ? "text-signal-positive" : "text-signal-negative";
        color2 = higherIsBetter ? "text-signal-negative" : "text-signal-positive";
      } else if (value2 > value1) {
        color1 = higherIsBetter ? "text-signal-negative" : "text-signal-positive";
        color2 = higherIsBetter ? "text-signal-positive" : "text-signal-negative";
      }
    }

    return (
      <div className="grid grid-cols-3 gap-4 py-3 border-b border-border-default items-center">
        <div className={`font-mono text-lg text-center ${color1}`}>{value1 !== undefined ? value1 : "-"}</div>
        <div className="flex flex-col items-center text-secondary gap-1">
          {Icon && <Icon className="w-4 h-4" />}
          <span className="text-xs uppercase tracking-wider font-medium">{label}</span>
        </div>
        <div className={`font-mono text-lg text-center ${color2}`}>{value2 !== undefined ? value2 : "-"}</div>
      </div>
    );
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-base/80 backdrop-blur-sm"
          onClick={onClose}
        />
        
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-4xl bg-surface-1 border border-border-default rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
        >
          <div className="flex items-center justify-between p-4 sm:p-6 border-b border-border-default">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-surface-2">
                <GitCompare className="w-5 h-5 text-secondary" />
              </div>
              <div>
                <h2 className="text-lg font-medium text-primary">Compare Companies</h2>
                <p className="text-sm text-tertiary">Select two entities to analyze side-by-side</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-surface-2 text-tertiary hover:text-primary transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 sm:p-6">
            {isLoading ? (
              <div className="flex items-center justify-center p-12">
                <Loader2 className="w-6 h-6 text-secondary animate-spin" />
              </div>
            ) : (
              <div className="space-y-8">
                {/* Selectors */}
                <div className="grid grid-cols-2 gap-8">
                  <div>
                    <label className="block text-xs font-mono uppercase tracking-wider text-secondary mb-2">Entity A</label>
                    <select 
                      className="w-full bg-surface-2 border border-border-default rounded-md px-3 py-2 text-primary focus:outline-none focus:border-border-strong"
                      value={selectedCompany1}
                      onChange={(e) => setSelectedCompany1(e.target.value)}
                    >
                      <option value="">Select a company...</option>
                      {companies?.map(c => (
                        <option key={`c1-${c.name}`} value={c.name}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-mono uppercase tracking-wider text-secondary mb-2">Entity B</label>
                    <select 
                      className="w-full bg-surface-2 border border-border-default rounded-md px-3 py-2 text-primary focus:outline-none focus:border-border-strong"
                      value={selectedCompany2}
                      onChange={(e) => setSelectedCompany2(e.target.value)}
                    >
                      <option value="">Select a company...</option>
                      {companies?.map(c => (
                        <option key={`c2-${c.name}`} value={c.name}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Comparison Data */}
                {company1 || company2 ? (
                  <div className="bg-surface-2/30 rounded-xl border border-border-default p-4 sm:p-6">
                    {renderMetric("Momentum Score", company1?.momentum_score, company2?.momentum_score, Activity, true)}
                    {renderMetric("Growth Score", company1?.growth_score, company2?.growth_score, TrendingUp, true)}
                    {renderMetric("Risk Score", company1?.risk_score, company2?.risk_score, AlertTriangle, false)}
                    {renderMetric("Business Health", company1?.business_health, company2?.business_health, Building2, true)}
                    {renderMetric("Funding Events", company1?.funding_events, company2?.funding_events, Activity, true)}
                    {renderMetric("Hiring Events", company1?.hiring_events, company2?.hiring_events, Activity, true)}
                    
                    {/* Recommendation Row */}
                    <div className="grid grid-cols-2 gap-8 mt-6 pt-4">
                      {company1 && (
                        <div className="text-center">
                          <span className="text-xs uppercase tracking-wider text-secondary block mb-2">Verdict</span>
                          <span className="inline-block px-3 py-1 rounded-full bg-surface-3 border border-border-strong text-primary text-sm">
                            {company1.recommendation}
                          </span>
                        </div>
                      )}
                      {company2 && (
                        <div className="text-center">
                          <span className="text-xs uppercase tracking-wider text-secondary block mb-2">Verdict</span>
                          <span className="inline-block px-3 py-1 rounded-full bg-surface-3 border border-border-strong text-primary text-sm">
                            {company2.recommendation}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12 text-tertiary">
                    Please select two companies to compare.
                  </div>
                )}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
