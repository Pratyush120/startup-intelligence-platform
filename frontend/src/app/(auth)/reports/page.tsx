"use client";

import { useRecommendations } from "@/hooks/use-intelligence";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, FileText, CheckCircle, ShieldAlert, Target } from "lucide-react";
import { useRouter } from "next/navigation";

export default function ReportsPage() {
  const { data: recommendations, isLoading, isError } = useRecommendations();
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center min-h-[50vh]">
        <div className="flex flex-col items-center text-muted-foreground gap-4">
          <Loader2 className="w-8 h-8 animate-spin" />
          <p>Generating strategic reports...</p>
        </div>
      </div>
    );
  }

  if (isError || !recommendations) {
    return (
      <div className="h-full flex items-center justify-center min-h-[50vh]">
        <div className="text-red-400">Failed to load strategy reports.</div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 flex flex-col">
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h1 className="text-3xl font-heading font-semibold tracking-tight">Strategy Reports</h1>
          <p className="text-muted-foreground mt-2 font-mono text-sm">AI-Generated Market Actions & Playbooks</p>
        </div>
      </div>

      <div className="space-y-6">
        {recommendations.length === 0 ? (
          <div className="p-12 text-center text-muted-foreground bg-card/40 rounded-xl border border-border">
            No strategic reports have been generated yet. Trigger a pipeline run to generate insights.
          </div>
        ) : (
          recommendations.map((rec) => (
            <Card key={rec.id} className="bg-card/40 backdrop-blur-sm border-border">
              <CardHeader className="flex flex-row items-start justify-between">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <Badge variant="outline" className={`font-mono bg-transparent ${
                      rec.priority === 'High' ? 'text-signal-danger border-signal-danger/30' :
                      rec.priority === 'Medium' ? 'text-yellow-500 border-yellow-500/30' :
                      'text-muted-foreground border-border'
                    }`}>
                      {rec.priority} Priority
                    </Badge>
                    <span className="text-xs text-muted-foreground font-mono">{new Date(rec.timestamp).toLocaleDateString()}</span>
                  </div>
                  <CardTitle className="text-xl">{rec.title}</CardTitle>
                  <CardDescription className="text-base mt-2">{rec.reason}</CardDescription>
                </div>
                <div className="flex flex-col items-end text-sm space-y-2 shrink-0">
                  <div className="font-mono text-muted-foreground">Confidence</div>
                  <div className="text-2xl font-bold text-signal-positive">{rec.confidence}%</div>
                </div>
              </CardHeader>
              
              <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium flex items-center gap-2 mb-2 text-muted-foreground">
                      <Target className="w-4 h-4" /> Recommended Action
                    </h4>
                    <p className="text-sm bg-muted/20 p-3 rounded-md border border-border/50">{rec.suggestedAction}</p>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium flex items-center gap-2 mb-2 text-muted-foreground">
                      <FileText className="w-4 h-4" /> Supporting Evidence
                    </h4>
                    <ul className="space-y-2 text-sm text-muted-foreground list-disc list-inside">
                      {rec.evidence.map((ev, i) => <li key={i}>{ev}</li>)}
                    </ul>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium flex items-center gap-2 mb-2 text-signal-positive">
                      <CheckCircle className="w-4 h-4" /> Estimated Opportunity
                    </h4>
                    <p className="text-sm text-muted-foreground">{rec.estimatedOpportunity}</p>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium flex items-center gap-2 mb-2 text-signal-danger">
                      <ShieldAlert className="w-4 h-4" /> Estimated Risk
                    </h4>
                    <p className="text-sm text-muted-foreground">{rec.estimatedRisk}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
