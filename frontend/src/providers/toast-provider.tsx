"use client";

import { Toaster } from "sonner";
import { useTheme } from "next-themes";

export function ToastProvider() {
  const { theme } = useTheme();

  return (
    <Toaster
      position="bottom-right"
      theme={theme as "light" | "dark" | "system" | undefined}
      toastOptions={{
        className: "bg-surface-1 border border-border-strong rounded-md text-primary text-sm shadow-2xl",
        descriptionClassName: "text-secondary text-sm",
      }}
    />
  );
}
