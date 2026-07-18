"""
Executive Intelligence Report Generator
"""

from collections import Counter


class ExecutiveReport:

    def generate(self, events, company_store):

        report = {}

        report["total_events"] = len(events)

        report["funding_events"] = sum(

            e.event_type == "Funding"

            for e in events

        )

        report["hiring_events"] = sum(

            e.event_type == "Hiring"

            for e in events

        )

        report["layoff_events"] = sum(

            e.event_type == "Layoff"

            for e in events

        )

        report["expansion_events"] = sum(

            e.event_type == "Expansion"

            for e in events

        )

        report["acquisition_events"] = sum(

            e.event_type == "Acquisition"

            for e in events

        )

        if company_store:

            companies = company_store.top_companies()

            report["top_companies"] = companies[:5]

        else:

            report["top_companies"] = []

        publishers = Counter(

            e.source

            for e in events

        )

        report["top_publishers"] = publishers.most_common(5)

        return report

    def print_report(self, report):

        print()

        print("=" * 70)

        print("EXECUTIVE INTELLIGENCE REPORT")

        print("=" * 70)

        print()

        print(f"Total Events        : {report['total_events']}")

        print(f"Funding Events      : {report['funding_events']}")

        print(f"Hiring Events       : {report['hiring_events']}")

        print(f"Layoff Events       : {report['layoff_events']}")

        print(f"Expansion Events    : {report['expansion_events']}")

        print(f"Acquisition Events  : {report['acquisition_events']}")

        print()

        print("=" * 70)

        print("TOP COMPANIES")

        print("=" * 70)

        print()

        for company in report["top_companies"]:

            print(

                f"{company.company_name:<20}"

                f"Momentum : {company.momentum_score:<4}"

                f"Funding : {company.latest_funding}"

            )

        print()

        print("=" * 70)

        print("TOP SOURCES")

        print("=" * 70)

        print()

        for source, count in report["top_publishers"]:

            print(f"{source:<20} {count}")