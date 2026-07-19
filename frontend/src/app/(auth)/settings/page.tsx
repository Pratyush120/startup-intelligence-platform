"use client";

import { usePipelineStatus, useRunPipeline } from "@/hooks/use-intelligence";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Database, Play, AlertCircle, CheckCircle2, Clock } from "lucide-react";
import { toast } from "sonner"; // Assuming sonner is used for toasts, standard in modern shadcn/next, or we can use native alert

export default function SettingsPage() {
  const { data: status, isLoading: loadingStatus } = usePipelineStatus();
  const runPipelineMutation = useRunPipeline();

  const handleRunPipeline = () => {
    toast?.("Pipeline triggered", {
      description: "Data ingestion process has started.",
    });
    runPipelineMutation.mutate(undefined, {
      onSuccess: () => {
        toast?.success("Pipeline execution complete");
      },
      onError: (err) => {
        toast?.error("Pipeline execution failed");
        console.error(err);
      }
    });
  };

  const isRunning = status?.status === "running" || runPipelineMutation.isPending;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 flex flex-col">
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h1 className="text-3xl font-heading font-semibold tracking-tight">System Settings</h1>
          <p className="text-muted-foreground mt-2 font-mono text-sm">Platform Configuration & Jobs</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="bg-card/40 backdrop-blur-sm border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="w-5 h-5 text-primary" />
              Intelligence Pipeline
            </CardTitle>
            <CardDescription>
              Manage background data collection and processing jobs.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex justify-between items-center p-4 bg-muted/20 border border-border rounded-lg">
              <div className="space-y-1">
                <div className="text-sm font-medium">Pipeline Status</div>
                <div className="text-xs text-muted-foreground">
                  {loadingStatus ? "Checking status..." :
                   status?.startedAt ? `Last run: ${new Date(status.startedAt).toLocaleString()}` :
                   "No pipeline history found."}
                </div>
              </div>
              <Badge variant="outline" className={`font-mono bg-transparent ${
                isRunning ? 'text-blue-400 border-blue-400/30' : 
                status?.status === 'failed' ? 'text-signal-danger border-signal-danger/30' :
                status?.status === 'success' ? 'text-signal-positive border-signal-positive/30' :
                'text-muted-foreground border-border'
              }`}>
                {isRunning ? (
                  <span className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
                    Running
                  </span>
                ) : status?.status || "Idle"}
              </Badge>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-muted/10 border border-border rounded-lg space-y-1">
                <div className="text-xs text-muted-foreground uppercase tracking-wider font-mono flex items-center gap-2">
                  <CheckCircle2 className="w-3 h-3" /> Records Processed
                </div>
                <div className="text-2xl font-semibold">{status?.recordsProcessed || 0}</div>
              </div>
              <div className="p-4 bg-muted/10 border border-border rounded-lg space-y-1">
                <div className="text-xs text-muted-foreground uppercase tracking-wider font-mono flex items-center gap-2">
                  <AlertCircle className="w-3 h-3" /> Errors
                </div>
                <div className="text-2xl font-semibold">{status?.errors || 0}</div>
              </div>
            </div>

            <div className="pt-2">
              <Button 
                onClick={handleRunPipeline} 
                disabled={isRunning}
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-medium"
              >
                {isRunning ? (
                  <>
                    <Clock className="w-4 h-4 mr-2 animate-spin" /> Processing Data...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 mr-2 fill-current" /> Trigger Manual Run
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Placeholder for other settings */}
        <Card className="bg-card/40 backdrop-blur-sm border-border opacity-50">
          <CardHeader>
            <CardTitle>API Configuration</CardTitle>
            <CardDescription>Manage external integration keys.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-muted-foreground italic">
              These settings are managed via environment variables in production mode.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
