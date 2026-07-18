import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center justify-center rounded-[3px] border border-border-default h-[24px] px-2 mono-sm transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-inverted hover:bg-primary/80",
        secondary:
          "border-transparent bg-surface-2 text-primary hover:bg-surface-2/80",
        destructive:
          "border-transparent bg-signal-danger text-white hover:bg-signal-danger/80",
        outline: "text-primary",
        positive: "border-transparent bg-signal-positive-subtle text-signal-positive border border-signal-positive/20",
        warning: "border-transparent bg-signal-warning-subtle text-signal-warning border border-signal-warning/20",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
