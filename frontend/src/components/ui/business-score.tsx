"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { motion } from "framer-motion"

interface BusinessScoreProps {
  score: number;
  momentum: number;
  className?: string;
}

export function BusinessScore({ score, momentum, className }: BusinessScoreProps) {
  // Determine color based on score or momentum, but keeping it muted as requested
  const isPositive = momentum > 0;
  const isNegative = momentum < 0;
  
  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="flex flex-col">
        <span className="text-2xl font-mono tracking-tight font-medium text-foreground">
          {score}
          <span className="text-muted-foreground text-sm ml-0.5">/100</span>
        </span>
      </div>
      <div className="flex flex-col gap-1 items-center justify-center">
        {/* Momentum Indicator - Elegant Simplicity */}
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded border border-border bg-card">
          <motion.div 
            className={cn(
              "w-1.5 h-1.5 rounded-full",
              isPositive ? "bg-signal-positive" : isNegative ? "bg-signal-danger" : "bg-signal-warning"
            )}
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          />
          <span className={cn(
            "text-xs font-mono font-medium",
            isPositive ? "text-signal-positive" : isNegative ? "text-signal-danger" : "text-signal-warning"
          )}>
            {momentum > 0 ? "+" : ""}{momentum}
          </span>
        </div>
      </div>
    </div>
  )
}
