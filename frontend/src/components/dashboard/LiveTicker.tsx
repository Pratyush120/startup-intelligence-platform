"use client";

import { motion } from "framer-motion";
import { TimelineEvent } from "@/lib/types/executive";
import { Activity } from "lucide-react";
import { useState, useEffect } from "react";

interface LiveTickerProps {
  events: TimelineEvent[];
}

export function LiveTicker({ events }: LiveTickerProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (!events.length) return;
    const interval = setInterval(() => {
      if (!events[currentIndex]) return;
      setCurrentIndex((prev) => (prev + 1) % events.length);
    }, 4000); // Cycle every 4 seconds
    return () => clearInterval(interval);
  }, [events.length, currentIndex]);

  if (!events.length) return null;

  const currentEvent = events[currentIndex];
  if (!currentEvent) return null;

  return (
    <div className="w-full bg-surface-1 border-y border-border-default h-10 flex items-center px-4 overflow-hidden relative text-sm">
      <div className="flex items-center gap-2 shrink-0 border-r border-border-default pr-4 mr-4 text-signal-intelligence">
        <Activity className="w-4 h-4 animate-pulse" />
        <span className="caption-sm uppercase font-bold tracking-widest text-primary">Live</span>
      </div>
      
      <div className="flex-1 overflow-hidden relative h-full flex items-center">
        <motion.div
          key={currentIndex}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -20, opacity: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="flex items-center gap-3 absolute w-full"
        >
          <span className="font-medium text-primary bg-surface-2 px-2 py-0.5 rounded-sm caption-sm">
            {currentEvent.companyName}
          </span>
          <span className="text-secondary uppercase caption-sm tracking-wider">
            {currentEvent.eventType}
          </span>
          <span className="text-primary truncate">
            {currentEvent.businessImpact}
          </span>
        </motion.div>
      </div>
    </div>
  );
}
