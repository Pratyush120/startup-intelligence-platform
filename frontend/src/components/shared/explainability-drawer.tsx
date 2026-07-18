"use client"

import * as React from "react"
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer"
import { Button } from "@/components/ui/button"
import { X, ArrowDown, Activity, AlignLeft, ShieldAlert, Cpu } from "lucide-react"

interface ExplainabilityDrawerProps {
  children?: React.ReactNode;
  trigger?: React.ReactNode;
  title: string;
}

export function ExplainabilityDrawer({ children, trigger, title }: ExplainabilityDrawerProps) {
  return (
    <Drawer direction="right">
      <DrawerTrigger asChild>
        {trigger || <Button variant="ghost" size="sm">View Mechanics</Button>}
      </DrawerTrigger>
      <DrawerContent className="h-screen top-0 right-0 left-auto mt-0 w-full sm:w-[480px] rounded-none border-l border-border bg-card text-card-foreground">
        <div className="flex h-full flex-col">
          <DrawerHeader className="border-b border-border flex items-center justify-between py-4">
            <div>
              <DrawerTitle className="text-base font-semibold font-sans">{title}</DrawerTitle>
              <DrawerDescription className="text-xs font-mono mt-1 text-muted-foreground">Audit Trail & Mechanics</DrawerDescription>
            </div>
            <DrawerClose asChild>
              <Button variant="ghost" className="w-full">
                Download Log
              </Button>
            </DrawerClose>
          </DrawerHeader>
          
          <div className="flex-1 overflow-auto p-6 space-y-8 relative">
            {/* Vertical timeline line */}
            <div className="absolute left-[39px] top-6 bottom-6 w-px bg-border z-0" />
            
            {/* Step 1 */}
            <div className="relative z-10 flex gap-4">
              <div className="w-8 h-8 rounded-full bg-muted border border-border flex flex-shrink-0 items-center justify-center mt-1">
                <Activity className="w-4 h-4 text-muted-foreground" />
              </div>
              <div className="space-y-2 flex-1">
                <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider">Step 1: Raw Data Collection</div>
                <div className="p-3 rounded-md bg-muted/50 border border-border">
                  <div className="text-sm font-medium mb-1">Source: Bloomberg Terminal</div>
                  <div className="text-sm text-muted-foreground line-clamp-2">"Nexus Robotics secures $120M Series C, pivots to autonomous warehouse logistics..."</div>
                </div>
              </div>
            </div>

            {/* Step 2 */}
            <div className="relative z-10 flex gap-4">
              <div className="w-8 h-8 rounded-full bg-muted border border-border flex flex-shrink-0 items-center justify-center mt-1">
                <AlignLeft className="w-4 h-4 text-muted-foreground" />
              </div>
              <div className="space-y-2 flex-1">
                <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider">Step 2: NLP Extraction</div>
                <div className="p-3 rounded-md bg-muted/50 border border-border space-y-2">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-muted-foreground">Vector:</span>
                    <span className="font-medium">Funding & Pivot</span>
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-muted-foreground">Sentiment:</span>
                    <span className="text-signal-positive font-medium font-mono">+0.85 (Positive)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Step 3 */}
            <div className="relative z-10 flex gap-4">
              <div className="w-8 h-8 rounded-full bg-signal-intelligence/10 border border-signal-intelligence/30 flex flex-shrink-0 items-center justify-center mt-1">
                <Cpu className="w-4 h-4 text-signal-intelligence" />
              </div>
              <div className="space-y-2 flex-1">
                <div className="text-xs font-mono text-muted-foreground uppercase tracking-wider text-signal-intelligence">Step 3: Feature Engineering</div>
                <div className="p-3 rounded-md bg-signal-intelligence/5 border border-signal-intelligence/20 space-y-2">
                  <div className="text-sm text-foreground">
                    Applied Weight: High Impact
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Target entity occupies a primary competitive node in the user's defined ontology.
                  </div>
                </div>
              </div>
            </div>

            {/* Step 4 */}
            <div className="relative z-10 flex gap-4">
              <div className="w-8 h-8 rounded-full bg-card border border-border flex flex-shrink-0 items-center justify-center mt-1 shadow-sm">
                <ShieldAlert className="w-4 h-4 text-foreground" />
              </div>
              <div className="space-y-2 flex-1">
                <div className="text-xs font-mono text-foreground uppercase tracking-wider font-semibold">Final Calculation</div>
                <div className="p-4 rounded-md border-l-2 border-l-signal-danger bg-muted/30 border-y border-r border-y-border border-r-border">
                  <div className="text-sm">Score Adjustment: <span className="font-mono text-signal-danger">-12 Points</span> (Threat Increase)</div>
                  <div className="text-sm mt-1">New Competitor Threat Level: <span className="font-medium">HIGH</span></div>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </DrawerContent>
    </Drawer>
  )
}
