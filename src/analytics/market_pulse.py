"""
Market Pulse Engine

Computes the overall state of the startup ecosystem from detected events.
"""

from collections import Counter
from dataclasses import dataclass


@dataclass
class PulseResult:
    funding: str
    hiring: str
    layoffs: str
    expansion: str
    acquisitions: str
    dominant_event: str
    total_events: int


class MarketPulseEngine:
    def calculate(self, events):

        counts = Counter()

        for event in events:
            counts[event.event_type] += 1

        def classify(count):

            if count >= 10:
                return "Strong"

            if count >= 5:
                return "Moderate"

            if count >= 1:
                return "Emerging"

            return "Quiet"

        dominant = "None"

        if counts:
            dominant = max(counts, key=counts.get)

        return PulseResult(
            funding=classify(counts["Funding"]),
            hiring=classify(counts["Hiring"]),
            layoffs=classify(counts["Layoff"]),
            expansion=classify(counts["Expansion"]),
            acquisitions=classify(counts["Acquisition"]),
            dominant_event=dominant,
            total_events=sum(counts.values()),
        )
