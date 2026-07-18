import { Sidebar } from "@/components/layout/sidebar";
import { TopAppBar } from "@/components/layout/TopAppBar";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen w-full bg-base overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col h-full relative overflow-hidden">
        <TopAppBar />
        <main className="flex-1 overflow-y-auto bg-base p-6 md:p-8 relative z-0">
          <div className="max-w-7xl mx-auto h-full">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
