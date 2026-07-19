"use client";

import { Search, Bell, Moon, Sun, User } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export function TopAppBar() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <header className="h-16 border-b border-border-default bg-base/80 backdrop-blur-md sticky top-0 z-sticky flex items-center justify-between px-6">
      
      {/* Global Search / Command Palette Trigger */}
      <div className="flex items-center flex-1">
        <button className="flex items-center gap-2 px-3 py-1.5 rounded-md border border-border-default bg-surface-1 text-secondary hover:text-primary hover:border-border-strong transition-colors w-[400px] group focus-visible:ring-2 focus-visible:ring-focus outline-none">
          <Search className="w-4 h-4" />
          <span className="text-sm">Analyze a company, market or competitor...</span>
          <kbd className="ml-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border border-border-default bg-base px-1.5 font-mono text-[10px] font-medium text-tertiary opacity-100 group-hover:opacity-100 transition-opacity">
            <span className="text-xs">⌘</span>K
          </kbd>
        </button>
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-4">
        <button 
          className="p-2 text-secondary hover:text-primary rounded-md hover:bg-surface-1 transition-colors focus-visible:ring-2 focus-visible:ring-focus outline-none relative"
          aria-label="Notifications"
        >
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-signal-danger border border-base"></span>
        </button>

        <button 
          className="p-2 text-secondary hover:text-primary rounded-md hover:bg-surface-1 transition-colors focus-visible:ring-2 focus-visible:ring-focus outline-none"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          aria-label="Toggle Theme"
        >
          {mounted && theme === "dark" ? (
            <Sun className="w-5 h-5" />
          ) : (
            <Moon className="w-5 h-5" />
          )}
        </button>

        <div className="h-6 w-px bg-border-default mx-2"></div>

        <button 
          className="flex items-center gap-2 p-1 pl-2 pr-3 rounded-full border border-border-default hover:border-border-strong transition-colors focus-visible:ring-2 focus-visible:ring-focus outline-none"
          aria-label="User Profile"
        >
          <div className="w-7 h-7 rounded-full bg-surface-2 flex items-center justify-center text-primary">
            <User className="w-4 h-4" />
          </div>
          <span className="text-sm font-medium text-primary">Executive</span>
        </button>
      </div>

    </header>
  );
}
