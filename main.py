"""
Strategic Decision Intelligence Platform

Main Entry Point — Phase 6 (Production Pipeline)
"""

import json
from src.pipeline.orchestrator import PipelineOrchestrator


def main():

    print("=" * 70)
    print("Strategic Decision Intelligence Platform")
    print("=" * 70)

    orchestrator = PipelineOrchestrator()
    result = orchestrator.run()

    meta = result.run_metadata

    print()
    print("=" * 70)
    print("Pipeline Summary")
    print("=" * 70)
    print(f"Run ID                  : {meta.get('run_id', '-')}")
    print(f"Status                  : {meta.get('status', 'unknown')}")
    print(f"Duration                : {meta.get('duration_seconds', 0):.1f}s")
    print(f"Records Collected       : {meta.get('records_collected', 0)}")
    print(f"Events Processed        : {meta.get('records_processed', 0)}")
    print(f"Companies Identified    : {meta.get('companies_identified', 0)}")
    print(f"Errors                  : {meta.get('errors', 0)}")
    print()

    if result.executive_brief:
        brief = result.executive_brief
        print("Executive Brief:")
        print(f"  Market Health         : {brief.get('marketHealthScore')}/100")
        print(f"  Investment Climate    : {brief.get('investmentClimate')}")
        print(f"  Risk Level            : {brief.get('riskLevel')}")
        print(f"  Growth Outlook        : {brief.get('growthOutlook')}")
        print(f"  Confidence Score      : {brief.get('confidenceScore')}%")
        print()
        print(f"  Primary Recommendation:")
        print(f"  {brief.get('primaryRecommendation')}")
        print()

    if result.top_companies:
        print(f"Top Companies ({len(result.top_companies)} tracked):")
        for c in result.top_companies[:5]:
            print(
                f"  {c['name']:<25} "
                f"Momentum: {c['momentum']:<6} "
                f"Risk: {c['riskScore']:<6} "
                f"→ {c['recommendation']}"
            )
        print()

    if result.timeline_events:
        print(f"Recent Intelligence ({len(result.timeline_events)} events):")
        for e in result.timeline_events[:5]:
            print(f"  [{e['importance']}] {e['companyName']}: {e['eventType']}")
        print()

    print("Pipeline completed successfully.")
    print("=" * 70)

    return result


if __name__ == "__main__":
    main()