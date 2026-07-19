"use client";

import { motion, Variants } from "framer-motion";
import { StrategicAlert } from "@/lib/types/executive";
import { AlertCard } from "./AlertCard";

interface StrategicAlertsProps {
  alerts: StrategicAlert[];
}

export function StrategicAlerts({ alerts }: StrategicAlertsProps) {
  // Only display the 3-5 highest priority alerts.
  // We assume the data layer sorts them, but we slice just in case.
  const displayAlerts = alerts.slice(0, 5);

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 10 },
    show: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
  };

  return (
    <section className="flex flex-col gap-4">
      <header className="flex items-center justify-between">
        <h2 className="heading-md text-primary">Strategic Alerts</h2>
        <span className="caption-sm text-secondary px-2 py-1 bg-surface-2 rounded-sm border border-border-default">
          {displayAlerts.length} Active High-Priority Events
        </span>
      </header>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="flex flex-col gap-2"
      >
        {displayAlerts.map((alert) => (
          <motion.div key={alert.id} variants={itemVariants}>
            <AlertCard alert={alert} />
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}
