import type { Variants } from "framer-motion";

export const SPRING_TAUGHT = {
  type: "spring" as const,
  stiffness: 400,
  damping: 30,
};

export const EASE_ENTER = [0.16, 1, 0.3, 1] as const;
export const EASE_EXIT = [0.7, 0, 0.84, 0] as const;

export const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

export const itemVariants: Variants = {
  hidden: { opacity: 0, y: 10 },
  show: {
    opacity: 1,
    y: 0,
    transition: SPRING_TAUGHT,
  },
};

export const drawerVariants = {
  enter: {
    x: "0%",
    transition: { duration: 0.25, ease: EASE_ENTER },
  },
  exit: {
    x: "100%",
    transition: { duration: 0.2, ease: EASE_EXIT },
  },
};

export const fadeVariants: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};
