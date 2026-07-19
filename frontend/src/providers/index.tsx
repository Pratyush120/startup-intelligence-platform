"use client";

import { ThemeProvider } from "./ThemeProvider";
import { QueryProvider } from "./QueryProvider";

import { OmniSearchDialog } from "@/components/shared/omni-search-dialog";
import { Toaster } from "sonner";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem={false}
      disableTransitionOnChange
    >
      <QueryProvider>
        {children}
        <OmniSearchDialog />
        <Toaster />
      </QueryProvider>
    </ThemeProvider>
  );
}
