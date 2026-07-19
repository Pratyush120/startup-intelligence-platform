"use client";

import { motion } from "framer-motion";
import { MetricCard } from "./MetricCard";
import { MetricCard as MetricCardType } from "@/lib/types/executive";

interface MetricGridProps {
  metrics: MetricCardType[];
}

export function MetricGrid({ metrics }: MetricGridProps) {
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants: any = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } }
  };

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="show"
      className="grid grid-cols-1 sm:grid-cols-2 gap-4"
    >
      {metrics.map((metric) => (
        <motion.div key={metric.id} variants={itemVariants}>
          <MetricCard data={metric} />
        </motion.div>
      ))}
    </motion.div>
  );
}
