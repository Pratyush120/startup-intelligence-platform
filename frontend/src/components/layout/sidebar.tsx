"use client";

import Link from "next/link";
import {
  LayoutDashboard,
  Building2,
  LineChart,
  FileText,
  Settings,
  Bot
} from "lucide-react";

import { useUIStore } from "@/store/ui.store";

export function Sidebar() {
  const openCopilot = useUIStore(state => state.openCopilot);
  
  return (
    <aside className="w-64 border-r border-border-default bg-surface-1 flex flex-col h-full">
      <div className="p-6">
        <div className="font-sans font-bold text-xl tracking-tight text-primary">SDIP</div>
        <div className="text-xs text-secondary tracking-widest uppercase mt-1">Intelligence Platform</div>
      </div>

      <nav className="flex-1 px-4 py-4 space-y-2">
        <Link 
          href="/"
          className="flex items-center gap-3 px-3 py-2 rounded-md bg-selection-bg text-primary font-medium"
        >
          <LayoutDashboard className="w-4 h-4" />
          Command Center
        </Link>
        <Link 
          href="/watchlist"
          className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-surface-2 text-secondary hover:text-primary transition-colors font-medium"
        >
          <Building2 className="w-4 h-4" />
          My Watchlist
        </Link>
        <Link 
          href="/reports"
          className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-surface-2 text-secondary hover:text-primary transition-colors font-medium"
        >
          <FileText className="w-4 h-4" />
          Reports Library
        </Link>
        <button 
          className="flex w-full items-center gap-3 px-3 py-2 rounded-md hover:bg-surface-2 text-secondary hover:text-primary transition-colors font-medium"
          onClick={() => openCopilot()}
        >
          <Bot className="w-4 h-4" />
          AI Copilot
        </button>
      </nav>

      <div className="p-4 mt-auto">
        <Link 
          href="/settings"
          className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-surface-2 text-secondary hover:text-primary transition-colors font-medium"
        >
          <Settings className="w-4 h-4" />
          Settings
        </Link>
      </div>
    </aside>
  );
}
