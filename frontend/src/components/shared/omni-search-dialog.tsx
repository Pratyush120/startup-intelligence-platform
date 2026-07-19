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
import { Compass, Target, Server, FileText, ArrowRight, Loader2, Activity } from "lucide-react"
import { useRouter } from "next/navigation"
import { useTopCompanies, useSearch } from "@/hooks/use-intelligence"
import { useDebounce } from "@/hooks/use-debounce"

export function OmniSearchDialog() {
  const [open, setOpen] = React.useState(false)
  const [query, setQuery] = React.useState("")
  const debouncedQuery = useDebounce(query, 300)
  const router = useRouter()
  
  const { data: topCompanies } = useTopCompanies();
  const { data: searchResults, isLoading: isSearching } = useSearch(debouncedQuery);

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

  const isQuerying = debouncedQuery.length >= 2;
  const companies = isQuerying ? searchResults?.companies : topCompanies;
  const events = searchResults?.events || [];

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput 
        placeholder="Search intelligence, entities, or commands..." 
        className="font-sans" 
        value={query}
        onValueChange={setQuery}
      />
      <CommandList className="bg-card/95 backdrop-blur-md">
        {isSearching && (
          <div className="p-4 flex items-center justify-center text-muted-foreground">
            <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Searching...
          </div>
        )}
        {!isSearching && <CommandEmpty>No results found.</CommandEmpty>}
        
        {(!isQuerying || (companies && companies.length > 0)) && (
          <CommandGroup heading={isQuerying ? "Companies" : "Top Entities"}>
            {companies?.map(company => (
              <CommandItem key={company.id} onSelect={() => runCommand(() => router.push(`/entities/${company.id}`))} className="cursor-pointer">
                <Server className="mr-2 h-4 w-4 text-muted-foreground" />
                <span>{company.name}</span>
                <div className="ml-auto text-xs font-mono text-muted-foreground">Company</div>
              </CommandItem>
            ))}
          </CommandGroup>
        )}

        {isQuerying && events.length > 0 && (
          <>
            <CommandSeparator />
            <CommandGroup heading="Intelligence Events">
              {events.map(event => (
                <CommandItem key={event.id} onSelect={() => runCommand(() => router.push(`/entities/${encodeURIComponent(event.companyName)}`))} className="cursor-pointer">
                  <Activity className="mr-2 h-4 w-4 text-muted-foreground" />
                  <div className="flex flex-col max-w-full overflow-hidden">
                     <span className="truncate">{event.aiSummary || event.businessImpact || event.eventType}</span>
                     <span className="text-xs text-muted-foreground truncate">{event.companyName}</span>
                  </div>
                  <div className="ml-auto text-xs font-mono text-muted-foreground pl-4">Event</div>
                </CommandItem>
              ))}
            </CommandGroup>
          </>
        )}

        {!isQuerying && (
          <>
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
          </>
        )}
        
        {/* Dynamic Preview Area */}
        <div className="border-t border-border p-4 bg-muted/20">
           <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider mb-2">Live Preview</div>
           <div className="text-sm font-medium">{query || 'Type "Compare Series A startups..."'}</div>
           <div className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
             Press Enter to execute intelligence command <ArrowRight className="w-3 h-3" />
           </div>
        </div>
      </CommandList>
    </CommandDialog>
  )
}
