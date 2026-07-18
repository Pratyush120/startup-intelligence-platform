import { SearchX, RefreshCcw } from "lucide-react";

interface EmptyStateProps {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({ title, description, actionLabel, onAction }: EmptyStateProps) {
  return (
    <div className="p-12 border border-dashed border-border-default rounded-md text-center bg-surface-1 flex flex-col items-center justify-center min-h-[300px]">
      <div className="w-12 h-12 rounded-full bg-surface-2 flex items-center justify-center mb-4">
        <SearchX className="w-6 h-6 text-tertiary" />
      </div>
      <h3 className="heading-sm text-primary mb-2">{title}</h3>
      <p className="body-sm text-secondary max-w-md mx-auto mb-6">
        {description}
      </p>
      {actionLabel && onAction && (
        <button 
          onClick={onAction}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-inverted rounded-md caption-md font-medium hover:opacity-90 transition-opacity focus-visible:ring-2 focus-visible:ring-focus outline-none"
        >
          <RefreshCcw className="w-4 h-4" />
          {actionLabel}
        </button>
      )}
    </div>
  );
}
