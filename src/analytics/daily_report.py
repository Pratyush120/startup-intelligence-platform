"""
Daily Intelligence Report
"""


class DailyReport:
    def generate(self, summary):

        report = []

        report.append("=" * 60)

        report.append("DAILY STARTUP INTELLIGENCE REPORT")

        report.append("=" * 60)

        report.append("")

        report.append(f"Total Business Events : {summary['total_events']}")

        report.append("")

        report.append("Business Events")

        report.append("----------------------------")

        for event, count in summary["event_breakdown"].items():
            report.append(f"{event:<20}{count}")

        report.append("")

        report.append("Most Active Companies")

        report.append("----------------------------")

        if summary["top_companies"]:
            for company, count in summary["top_companies"]:
                report.append(f"{company:<25}{count}")

        else:
            report.append("No company intelligence available.")

        report.append("")

        report.append("=" * 60)

        return "\n".join(report)
