"""
Analytics Engine

Converts Business Events into Business Metrics.
"""

from collections import Counter


class AnalyticsEngine:
    def summarize(self, events):

        summary = {}

        summary["total_events"] = len(events)

        counter = Counter()

        company_counter = Counter()

        for event in events:
            counter[event.event_type] += 1

            if event.company:
                company_counter[event.company] += 1

        summary["event_breakdown"] = dict(counter)

        summary["top_companies"] = company_counter.most_common(10)

        return summary
