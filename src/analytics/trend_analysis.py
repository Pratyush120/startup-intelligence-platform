"""
Trend Analysis

Analyses business events and identifies key ecosystem trends.
"""

from collections import Counter


class TrendAnalysisEngine:
    def analyze(self, events):

        counts = Counter()

        for event in events:
            counts[event.event_type] += 1

        trends = []

        if counts["Funding"] > counts["Layoff"]:
            trends.append("Funding activity exceeds layoffs.")

        if counts["Hiring"] > 0:
            trends.append("Companies continue hiring.")

        if counts["Expansion"] > 0:
            trends.append("Expansion activity detected.")

        if counts["Acquisition"] > 0:
            trends.append("M&A activity detected.")

        if not trends:
            trends.append("No significant trends identified.")

        return trends
