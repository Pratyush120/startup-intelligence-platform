"use client"

import * as React from "react"
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command"
import { Compass, Target, Server, FileText, ArrowRight } from "lucide-react"
import { useRouter } from "next/navigation"

export function OmniSearchDialog() {
  const [open, setOpen] = React.useState(false)
  const router = useRouter()

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [])

  const runCommand = React.useCallback((command: () => void) => {
    setOpen(false)
    command()
  }, [])

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Search intelligence, entities, or commands..." className="font-sans" />
      <CommandList className="bg-card/95 backdrop-blur-md">
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Entities">
          <CommandItem onSelect={() => runCommand(() => router.push('/entities/ent-nexus'))} className="cursor-pointer">
            <Server className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Nexus Robotics</span>
            <div className="ml-auto text-xs font-mono text-muted-foreground">Supply Chain AI</div>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push('/entities/ent-stratos'))} className="cursor-pointer">
            <Server className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Stratos Financial</span>
            <div className="ml-auto text-xs font-mono text-muted-foreground">FinTech</div>
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Commands">
          <CommandItem onSelect={() => runCommand(() => router.push('/'))} className="cursor-pointer">
            <FileText className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>View Morning Brief</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push('/radar'))} className="cursor-pointer">
            <Compass className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Open Market Radar</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push('/strategy'))} className="cursor-pointer">
            <Target className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Generate Strategy Report</span>
          </CommandItem>
        </CommandGroup>
        
        {/* Dynamic Preview Area (Mocked for OS feel) */}
        <div className="border-t border-border p-4 bg-muted/20">
           <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider mb-2">Live Preview</div>
           <div className="text-sm font-medium">Type "Compare Series A startups..."</div>
           <div className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
             Press Enter to execute intelligence command <ArrowRight className="w-3 h-3" />
           </div>
        </div>
      </CommandList>
    </CommandDialog>
  )
}
