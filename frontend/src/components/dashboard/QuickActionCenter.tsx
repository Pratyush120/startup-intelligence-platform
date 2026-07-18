"use client";

import { motion } from "framer-motion";
import { FileText, GitCompare, RefreshCw, Download, LineChart, Search } from "lucide-react";

export function QuickActionCenter() {
  const actions = [
    { id: 'report', label: 'Generate Report', icon: FileText, shortcut: '⌘R' },
    { id: 'compare', label: 'Compare Companies', icon: GitCompare, shortcut: '⌘C' },
    { id: 'refresh', label: 'Refresh Intelligence', icon: RefreshCw, shortcut: '⌘⇧R' },
    { id: 'export', label: 'Export PDF', icon: Download, shortcut: '⌘E' },
    { id: 'analyze', label: 'Analyze Entity', icon: Search, shortcut: '⌘F' },
    { id: 'market', label: 'View Market', icon: LineChart, shortcut: '⌘M' },
  ];

  return (
    <section className="bg-surface-1 border border-border-default rounded-md p-4">
      <div className="flex items-center gap-2 overflow-x-auto pb-2 sm:pb-0 scrollbar-hide">
        {actions.map(action => (
          <motion.button
            key={action.id}
            whileHover={{ y: -1 }}
            whileTap={{ y: 0 }}
            className="shrink-0 flex items-center gap-2 px-4 py-2 rounded-md bg-base border border-border-default text-secondary hover:text-primary hover:border-border-strong transition-colors focus-visible:ring-2 focus-visible:ring-focus outline-none group relative"
            title={`${action.label} (${action.shortcut})`}
          >
            <action.icon className="w-4 h-4 text-tertiary group-hover:text-primary transition-colors" />
            <span className="caption-md font-medium">{action.label}</span>
          </motion.button>
        ))}
      </div>
    </section>
  );
}
