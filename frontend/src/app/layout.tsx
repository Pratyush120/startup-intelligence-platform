import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/providers";

export const metadata: Metadata = {
  title: "SDIP | Strategic Decision Intelligence Platform",
  description: "Executive operating system for strategic decision making.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="font-sans antialiased overflow-hidden">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
