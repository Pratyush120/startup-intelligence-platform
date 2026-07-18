import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex shrink-0 items-center justify-center whitespace-nowrap transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-3 focus-visible:ring-offset-base disabled:pointer-events-none disabled:opacity-40 select-none [&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-inverted caption-md uppercase tracking-[0.06em] rounded-none hover:bg-primary/90",
        ghost: "bg-transparent border border-border-default text-secondary body-sm rounded-[3px] hover:border-border-strong hover:text-primary",
        text: "bg-transparent text-secondary body-sm hover:underline underline-offset-3 rounded-sm",
        destructive: "bg-destructive text-white rounded-none hover:bg-destructive/90",
      },
      size: {
        default: "h-[44px] px-6",
        sm: "h-[36px] px-4",
        icon: "h-9 w-9",
      },
    },
    compoundVariants: [
      {
        variant: "ghost",
        size: "default",
        className: "h-[36px] px-4", // Override for ghost
      },
      {
        variant: "text",
        size: "default",
        className: "h-auto px-0 py-0", // Override for text button
      }
    ],
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
