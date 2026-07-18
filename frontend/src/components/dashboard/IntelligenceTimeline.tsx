"use client";

import { motion } from "framer-motion";
import { TimelineEvent } from "@/lib/types/executive";
import { format, isToday, isYesterday } from "date-fns";

interface IntelligenceTimelineProps {
  events: TimelineEvent[];
}

export function IntelligenceTimeline({ events }: IntelligenceTimelineProps) {
  // Sort and group events
  const sortedEvents = [...events].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  
  const groupedEvents = sortedEvents.reduce((acc, event) => {
    const d = new Date(event.date);
    let group = format(d, 'MMMM d, yyyy');
    if (isToday(d)) group = 'Today';
    else if (isYesterday(d)) group = 'Yesterday';
    
    if (!acc[group]) acc[group] = [];
    acc[group]!.push(event);
    return acc;
  }, {} as Record<string, TimelineEvent[]>);

  const getPriorityColor = (priority: TimelineEvent["importance"]) => {
    switch (priority) {
      case "Critical": return "bg-signal-danger border-signal-danger";
      case "High": return "bg-signal-warning border-signal-warning";
      case "Medium": return "bg-signal-intelligence border-signal-intelligence";
      case "Low": return "bg-tertiary border-border-strong";
      default: return "bg-tertiary border-border-strong";
    }
  };

  return (
    <section className="flex flex-col gap-6">
      <header className="flex items-center justify-between">
        <h2 className="heading-md text-primary">Recent Intelligence</h2>
      </header>

      <div className="flex flex-col">
        {Object.entries(groupedEvents).map(([group, groupEvents], groupIdx) => (
          <div key={group} className="relative pb-8 last:pb-0">
            {/* Timeline Line */}
            {groupIdx !== Object.keys(groupedEvents).length - 1 && (
              <div className="absolute top-8 bottom-0 left-[11px] w-px bg-border-default -z-10" />
            )}
            
            <h3 className="caption-sm text-tertiary uppercase tracking-wider mb-4 ml-8 bg-base inline-block px-2">
              {group}
            </h3>

            <div className="flex flex-col gap-6">
              {groupEvents.map((event, i) => (
                <motion.div 
                  key={event.id}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, margin: "-50px" }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-start gap-4 group"
                >
                  <div className={`w-[23px] h-[23px] rounded-full shrink-0 border-4 border-base ${getPriorityColor(event.importance)} z-10 mt-1`} />
                  
                  <div className="flex-1 bg-surface-1 border border-border-default rounded-md p-4 group-hover:border-border-strong transition-colors">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <span className="caption-sm font-bold bg-surface-2 text-primary px-2 py-0.5 rounded-sm">
                        {event.companyName}
                      </span>
                      <span className="caption-sm text-secondary uppercase tracking-wider">
                        {event.eventType}
                      </span>
                      <span className="caption-sm text-tertiary ml-auto hidden sm:block">
                        {format(new Date(event.date), 'h:mm a')}
                      </span>
                    </div>
                    <p className="body-sm text-primary font-medium mb-1">{event.businessImpact}</p>
                    <p className="caption-sm text-secondary leading-relaxed border-l-2 border-border-strong pl-3 mt-2">
                      {event.aiSummary}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
