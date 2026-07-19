import Link from "next/link";
import {
  LayoutDashboard,
  Building2,
  LineChart,
  FileText,
  Settings
} from "lucide-react";

export function Sidebar() {
  return (
    <aside className="w-64 border-r border-border-default bg-surface-1 flex flex-col h-full">
      <div className="p-6">
        <div className="font-sans font-bold text-xl tracking-tight text-primary">SDIP</div>
        <div className="text-xs text-secondary tracking-widest uppercase mt-1">Intelligence Platform</div>
      </div>

      <nav className="flex-1 px-4 py-4 space-y-2">
        <Link 
          href="/dashboard"
          className="flex items-center gap-3 px-3 py-2 rounded-md bg-selection-bg text-primary font-medium"
        >
          <LayoutDashboard className="w-4 h-4" />
          Command Center
        </Link>
        <Link 
          href="/companies"
          className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-surface-2 text-secondary hover:text-primary transition-colors font-medium"
        >
          <Building2 className="w-4 h-4" />
          Companies
        </Link>
        <Link 
          href="/market"
          className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-surface-2 text-secondary hover:text-primary transition-colors font-medium"
        >
          <LineChart className="w-4 h-4" />
          Market Intelligence
        </Link>
        <Link 
          href="/reports"
          className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-surface-2 text-secondary hover:text-primary transition-colors font-medium"
        >
          <FileText className="w-4 h-4" />
          Strategy Reports
        </Link>
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
