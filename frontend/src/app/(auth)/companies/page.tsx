"use client";

import { useTopCompanies } from "@/hooks/use-intelligence";
import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Loader2, Building2 } from "lucide-react";
import { BusinessScore } from "@/components/ui/business-score";

export default function CompaniesPage() {
  const { data: companies, isLoading, isError } = useTopCompanies();
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center min-h-[50vh]">
        <div className="flex flex-col items-center text-muted-foreground gap-4">
          <Loader2 className="w-8 h-8 animate-spin" />
          <p>Loading companies directory...</p>
        </div>
      </div>
    );
  }

  if (isError || !companies) {
    return (
      <div className="h-full flex items-center justify-center min-h-[50vh]">
        <div className="text-red-400">Failed to load companies data.</div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-heading font-semibold tracking-tight">Companies Directory</h1>
          <p className="text-muted-foreground mt-2 font-mono text-sm">Monitored Entities & Strategic Scores</p>
        </div>
      </div>

      <div className="border border-border rounded-xl overflow-hidden bg-card/40 backdrop-blur-sm">
        <table className="w-full text-sm text-left">
          <thead className="text-xs font-mono text-muted-foreground bg-muted/30 border-b border-border">
            <tr>
              <th className="px-6 py-4 font-medium">Entity Name</th>
              <th className="px-6 py-4 font-medium text-right">Funding Total</th>
              <th className="px-6 py-4 font-medium text-right">Growth Score</th>
              <th className="px-6 py-4 font-medium text-right">Risk Score</th>
              <th className="px-6 py-4 font-medium">Recommendation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {companies.length === 0 ? (
              <tr>
                <td colSpan={5} className="p-8 text-center text-muted-foreground">
                  No companies found in the database.
                </td>
              </tr>
            ) : (
              companies.map((company) => (
                <tr 
                  key={company.id} 
                  onClick={() => router.push(`/entities/${company.id}`)}
                  className="hover:bg-muted/30 transition-colors cursor-pointer group"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded bg-muted flex items-center justify-center font-bold text-muted-foreground group-hover:text-foreground transition-colors">
                        <Building2 className="w-4 h-4" />
                      </div>
                      <span className="font-medium group-hover:text-primary transition-colors">{company.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right font-mono text-muted-foreground">
                    ${(company.fundingTotal / 1000000).toFixed(1)}M
                  </td>
                  <td className="px-6 py-4 text-right">
                    <BusinessScore score={company.growthScore} momentum={company.momentum} />
                  </td>
                  <td className="px-6 py-4 text-right font-mono">
                    <span className={company.riskScore > 75 ? "text-signal-danger" : company.riskScore > 50 ? "text-yellow-500" : "text-signal-positive"}>
                      {company.riskScore}/100
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <Badge variant="outline" className={`font-mono bg-transparent ${
                      company.recommendation?.includes('Buy') ? 'text-signal-positive border-signal-positive/30' : 
                      company.recommendation?.includes('Sell') ? 'text-signal-danger border-signal-danger/30' : 
                      'text-muted-foreground border-border'
                    }`}>
                      {company.recommendation || "Neutral"}
                    </Badge>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
