"use client"

import * as React from "react"
import { Bell, Search, Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export function TopBar() {
  const { setTheme, theme } = useTheme()

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-border bg-card">
      <div className="flex-1" />
      
      <div className="flex-1 flex justify-center">
        <button className="w-full max-w-md flex items-center justify-between px-4 py-2 bg-input/50 hover:bg-input border border-border rounded-md text-sm text-muted-foreground transition-colors group">
          <div className="flex items-center gap-2">
            <Search className="w-4 h-4 text-muted-foreground group-hover:text-foreground transition-colors" />
            <span>Search intelligence, entities, or commands...</span>
          </div>
          <kbd className="hidden sm:inline-flex h-5 items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
            <span className="text-xs">⌘</span>K
          </kbd>
        </button>
      </div>

      <div className="flex-1 flex justify-end items-center gap-4">
        <button
          onClick={() => setTheme(theme === "light" ? "dark" : "light")}
          className="p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-accent"
        >
          <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute top-[1.2rem] h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </button>
        <button className="p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-accent relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-signal-danger rounded-full border border-card" />
        </button>
        <div className="w-8 h-8 rounded-full bg-accent border border-border flex items-center justify-center text-sm font-medium">
          CX
        </div>
      </div>
    </header>
  )
}
