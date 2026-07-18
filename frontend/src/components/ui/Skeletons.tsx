import { motion } from "framer-motion";

export function SkeletonLine({ className }: { className?: string }) {
  return (
    <div className={`bg-surface-2 rounded-sm animate-pulse ${className}`} />
  );
}

export function SkeletonCard() {
  return (
    <div className="bg-surface-1 border border-border-default rounded-md p-5 flex flex-col gap-4">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-sm bg-surface-2 animate-pulse shrink-0" />
        <SkeletonLine className="w-24 h-4" />
      </div>
      <div className="mt-2">
        <SkeletonLine className="w-16 h-8 mb-3" />
        <SkeletonLine className="w-32 h-3" />
      </div>
    </div>
  );
}

export function SkeletonDashboard() {
  return (
    <div className="flex flex-col gap-10">
      {/* Hero Skeleton */}
      <div className="bg-surface-1 border border-border-default rounded-md p-8 flex flex-col gap-6">
        <SkeletonLine className="w-48 h-8" />
        <div className="flex flex-col gap-3">
          <SkeletonLine className="w-full h-4" />
          <SkeletonLine className="w-3/4 h-4" />
        </div>
        <div className="bg-surface-2 p-5 rounded-md flex gap-4 mt-2">
          <div className="w-1.5 h-10 bg-border-strong rounded-full shrink-0" />
          <div className="flex flex-col gap-2 w-full">
            <SkeletonLine className="w-32 h-4" />
            <SkeletonLine className="w-full h-4" />
          </div>
        </div>
      </div>

      {/* Grid Skeletons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    </div>
  );
}
