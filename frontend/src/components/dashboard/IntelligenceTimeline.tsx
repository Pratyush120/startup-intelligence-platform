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
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - d.getTime()) / (1000 * 3600 * 24));
    
    let group = 'Older';
    if (isToday(d)) group = 'Today';
    else if (isYesterday(d)) group = 'Yesterday';
    else if (diffDays <= 7) group = 'Last Week';
    else if (diffDays <= 30) group = 'Last Month';
    
    if (!acc[group]) acc[group] = [];
    acc[group]!.push(event);
    return acc;
  }, {} as Record<string, TimelineEvent[]>);

  const getPriorityColor = (priority: TimelineEvent["importance"]) => {
    switch (priority) {
      case "Critical": return "bg-signal-danger border-signal-danger/30 text-signal-danger";
      case "High": return "bg-yellow-500 border-yellow-500/30 text-yellow-500";
      case "Medium": return "bg-blue-400 border-blue-400/30 text-blue-400";
      case "Low": return "bg-muted-foreground border-border text-muted-foreground";
      default: return "bg-muted-foreground border-border text-muted-foreground";
    }
  };

  // Ensure ordered rendering
  const groupOrder = ['Today', 'Yesterday', 'Last Week', 'Last Month', 'Older'];
  const orderedGroups = Object.entries(groupedEvents).sort((a, b) => groupOrder.indexOf(a[0]) - groupOrder.indexOf(b[0]));

  return (
    <section className="flex flex-col gap-6">
      <div className="flex flex-col">
        {orderedGroups.map(([group, groupEvents], groupIdx) => (
          <div key={group} className="relative pb-10 last:pb-0">
            {/* Timeline Line */}
            {groupIdx !== orderedGroups.length - 1 && (
              <div className="absolute top-10 bottom-0 left-[15px] w-px bg-border -z-10" />
            )}
            
            <h3 className="text-xs font-mono text-muted-foreground uppercase tracking-widest mb-6 ml-10 bg-background inline-block">
              {group}
            </h3>

            <div className="flex flex-col gap-8">
              {groupEvents.map((event, i) => {
                const priorityClasses = getPriorityColor(event.importance);
                return (
                <motion.div 
                  key={event.id}
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-50px" }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-start gap-6 group relative"
                >
                  <div className={`w-[11px] h-[11px] rounded-full shrink-0 border-2 bg-background z-10 mt-2 ml-[10px] ${priorityClasses.split(' ')[1]}`} />
                  
                  <div className="flex-1 bg-card/40 backdrop-blur-sm border border-border rounded-xl p-5 group-hover:border-primary/30 transition-all hover:shadow-lg">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-bold text-foreground">
                            {event.companyName}
                          </span>
                          <span className="text-xs text-muted-foreground uppercase tracking-wider font-mono px-2 py-0.5 bg-muted/30 rounded-full border border-border">
                            {event.eventType}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className={`text-[10px] uppercase font-mono tracking-wider px-2 py-1 rounded-sm border bg-transparent ${priorityClasses}`}>
                          {event.importance}
                        </span>
                        <span className="text-xs text-muted-foreground font-mono">
                          {format(new Date(event.date), 'MMM d, h:mm a')}
                        </span>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="p-3 bg-muted/20 border border-border/50 rounded-md">
                        <p className="text-sm font-medium mb-1">AI Analysis & Business Implication</p>
                        <p className="text-sm leading-relaxed text-muted-foreground">
                          {event.businessImpact}
                        </p>
                      </div>
                      
                      {event.aiSummary && (
                        <p className="text-sm leading-relaxed text-foreground border-l-2 border-primary/50 pl-3">
                          {event.aiSummary}
                        </p>
                      )}
                    </div>
                  </div>
                </motion.div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
