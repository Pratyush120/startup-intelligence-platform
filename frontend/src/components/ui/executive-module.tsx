"use client"

import * as React from "react"
import { ExecutiveModuleData } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { ArrowRight, CircleCheckBig, MoveRight } from "lucide-react"
import { ExplainabilityDrawer } from "@/components/shared/explainability-drawer"

interface ExecutiveModuleProps {
  data: ExecutiveModuleData;
}

export function ExecutiveModule({ data }: ExecutiveModuleProps) {
  return (
    <article className="py-12 border-b border-border-default last:border-0 relative">
      {/* Question */}
      <h2 className="display-md tracking-tight text-primary mb-8">
        {data.question}
      </h2>

      {/* Answer */}
      <div className="pl-6 border-l-2 border-primary mb-12">
        <p className="body-xl font-medium text-secondary max-w-3xl">
          {data.answer}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-12 items-start mb-12">
        
        {/* Evidence */}
        <div className="md:col-span-8 space-y-6">
          <h3 className="mono-sm text-secondary mb-4">Supporting Evidence</h3>
          <div className="space-y-4">
            {data.evidence.map((ev, i) => (
              <div key={i} className="flex gap-4 group">
                 <div className="w-1.5 h-1.5 rounded-full bg-signal-intelligence mt-2 shrink-0 opacity-50 group-hover:opacity-100 transition-opacity" />
                 <div>
                   <p className="body-md text-primary">{ev.dataPoint}</p>
                   <p className="mono-md text-secondary mt-1">{ev.source}</p>
                 </div>
              </div>
            ))}
          </div>
        </div>

        {/* Confidence & Action */}
        <div className="md:col-span-4 space-y-8 md:pl-8 md:border-l md:border-border-default">
           <div>
             <h3 className="mono-sm text-secondary mb-3">AI Confidence</h3>
             <div className="flex items-center gap-3">
               <span className="display-lg font-mono tracking-tighter text-primary">{data.confidence}%</span>
               <CircleCheckBig className="w-5 h-5 text-signal-positive" />
             </div>
             <div className="mt-3">
                <ExplainabilityDrawer 
                  title="Confidence Logic"
                  trigger={
                    <button className="caption-md text-signal-intelligence hover:underline underline-offset-4 flex items-center gap-1 transition-all">
                      Review Computation <ArrowRight className="w-3 h-3" />
                    </button>
                  }
                />
             </div>
           </div>

           <div>
             <Button className="w-full justify-between group">
                {data.action.label}
                <MoveRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
             </Button>
           </div>
        </div>
      </div>
    </article>
  )
}
