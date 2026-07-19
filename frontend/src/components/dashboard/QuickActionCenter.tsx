"use client";

import { motion } from "framer-motion";
import { FileText, GitCompare, RefreshCw, Download, LineChart, Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { useRunPipeline } from "@/hooks/use-intelligence";
import { useState } from "react";
import { CompareCompaniesModal } from "./CompareCompaniesModal";
import { toast } from "sonner";
import { useUIStore } from "@/store/ui.store";

export function QuickActionCenter() {
  const router = useRouter();
  const runPipelineMutation = useRunPipeline();
  const { openSearch, openCompare } = useUIStore();

  const handleAction = (id: string) => {
    switch (id) {
      case 'report':
        router.push('/reports');
        break;
      case 'compare':
        openCompare();
        break;
      case 'refresh':
        toast("Pipeline triggered", { description: "Data ingestion process has started in the background." });
        runPipelineMutation.mutate(undefined, {
          onSuccess: () => toast.success("Pipeline execution complete"),
          onError: () => toast.error("Pipeline execution failed")
        });
        break;
      case 'export':
        {
          const content = "Startup Intelligence Platform\n============================\n\nExecutive Market Brief\n\nGenerated: " + new Date().toLocaleString() + "\n\nThis is an automated export of the current intelligence metrics.";
          const blob = new Blob([content], { type: "text/plain" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "executive_brief.txt";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
          toast.success("Document exported successfully");
        }
        break;
      case 'analyze':
        openSearch();
        break;
      case 'market':
        router.push('/market');
        break;
    }
  };

  const actions = [
    { id: 'report', label: 'Generate Report', icon: FileText, shortcut: '⌘R' },
    { id: 'compare', label: 'Compare Companies', icon: GitCompare, shortcut: '⌘C' },
    { id: 'refresh', label: 'Refresh Intelligence', icon: RefreshCw, shortcut: '⌘⇧R' },
    { id: 'export', label: 'Export Document', icon: Download, shortcut: '⌘E' },
    { id: 'analyze', label: 'Analyze Entity', icon: Search, shortcut: '⌘F' },
    { id: 'market', label: 'View Market', icon: LineChart, shortcut: '⌘M' },
  ];

  return (
    <>
    <section className="bg-surface-1 border border-border-default rounded-md p-4">
      <div className="flex items-center gap-2 overflow-x-auto pb-2 sm:pb-0 scrollbar-hide">
        {actions.map(action => (
          <motion.button
            key={action.id}
            onClick={() => handleAction(action.id)}
            whileHover={{ y: -1 }}
            whileTap={{ y: 0 }}
            className="shrink-0 flex items-center gap-2 px-4 py-2 rounded-md bg-base border border-border-default text-secondary hover:text-primary hover:border-border-strong transition-colors focus-visible:ring-2 focus-visible:ring-focus outline-none group relative"
            title={`${action.label} (${action.shortcut})`}
          >
            <action.icon className={`w-4 h-4 text-tertiary group-hover:text-primary transition-colors ${action.id === 'refresh' && runPipelineMutation.isPending ? 'animate-spin' : ''}`} />
            <span className="caption-md font-medium">{action.label}</span>
          </motion.button>
        ))}
      </div>
    </section>
      <CompareCompaniesModal />
    </>
  );
}
