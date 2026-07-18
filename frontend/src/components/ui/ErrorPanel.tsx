import { AlertOctagon, RefreshCcw, Mail } from "lucide-react";

interface ErrorPanelProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  onContactSupport?: () => void;
}

export function ErrorPanel({ 
  title = "System Error", 
  message, 
  onRetry,
  onContactSupport 
}: ErrorPanelProps) {
  return (
    <div className="p-8 border border-signal-danger/20 rounded-md bg-signal-danger-subtle flex items-start gap-4">
      <AlertOctagon className="w-6 h-6 text-signal-danger shrink-0 mt-0.5" />
      <div className="flex-1">
        <h3 className="heading-sm text-signal-danger mb-1">{title}</h3>
        <p className="body-sm text-secondary mb-4">{message}</p>
        
        <div className="flex items-center gap-3">
          {onRetry && (
            <button 
              onClick={onRetry}
              className="px-4 py-2 bg-base border border-border-default hover:border-border-strong text-primary rounded-md caption-md font-medium transition-colors flex items-center gap-2 focus-visible:ring-2 focus-visible:ring-focus outline-none"
            >
              <RefreshCcw className="w-4 h-4" />
              Retry Connection
            </button>
          )}
          {onContactSupport && (
            <button 
              onClick={onContactSupport}
              className="px-4 py-2 bg-transparent text-secondary hover:text-primary rounded-md caption-md font-medium transition-colors flex items-center gap-2 focus-visible:ring-2 focus-visible:ring-focus outline-none"
            >
              <Mail className="w-4 h-4" />
              Support
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
