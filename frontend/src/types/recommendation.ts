export interface EvidenceItem {
  dataPoint: string;
  source: string;
}

export interface ExecutiveAction {
  label: string;
  intent: string;
}

export interface Recommendation {
  id: string;
  question: string;
  answer: string;
  evidence: EvidenceItem[];
  confidence: number;
  action: ExecutiveAction;
}
