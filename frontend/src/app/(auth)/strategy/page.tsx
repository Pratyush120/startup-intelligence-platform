"use client";

import { Button } from "@/components/ui/button"
import { ExecutiveModule } from "@/components/ui/executive-module"
import { FileText, Play } from "lucide-react"
import { useExecutiveModules } from "@/hooks/use-intelligence"

export default function StrategyPage() {
  const { data: modules, isLoading, isError } = useExecutiveModules();

  return (
    <div className="p-8 lg:p-16 max-w-5xl mx-auto space-y-16">
      
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-8 border-b border-border/40 pb-8">
        <div>
          <h1 className="text-4xl lg:text-5xl font-heading font-semibold tracking-tight">Strategy Room</h1>
          <p className="text-muted-foreground mt-4 font-mono text-sm tracking-wider uppercase">
            Active Scenarios & Briefs
          </p>
        </div>
        <div className="flex gap-4 shrink-0">
           <Button variant="ghost" className="gap-2 rounded-sm h-10 px-6 font-mono text-xs uppercase tracking-wider">
             <FileText className="w-4 h-4" /> Export All
           </Button>
           <Button className="bg-foreground text-background hover:bg-foreground/90 gap-2 rounded-sm h-10 px-6 font-mono text-xs uppercase tracking-wider">
             <Play className="w-4 h-4" /> Run Query
           </Button>
        </div>
      </header>

      {/* Scenarios Flow - Typography Driven */}
      <section>
         <div className="flex items-center gap-3 text-muted-foreground mb-8">
           <span className="text-sm font-mono font-medium uppercase tracking-widest">Active Intelligence Queries</span>
         </div>
         
         <div className="flex flex-col space-y-8">
           {isLoading ? (
             <div className="space-y-8">
               {[1, 2].map(i => (
                 <div key={i} className="h-48 bg-slate-900 animate-pulse rounded-xl border border-white/10" />
               ))}
             </div>
           ) : isError ? (
             <div className="text-red-400">Failed to load strategy modules.</div>
           ) : modules?.map(module => (
             <ExecutiveModule key={module.id} data={module} />
           ))}
         </div>
      </section>

    </div>
  )
}
