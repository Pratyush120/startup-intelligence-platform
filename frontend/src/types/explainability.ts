export interface AuditStep {
  stepNumber: number;
  label: string;
  heading: string;
  content: string;
  engineName?: string;
  sourceUrl?: string;
}

export interface ExplainabilityData {
  moduleId: string;
  moduleName: string;
  steps: AuditStep[];
}
