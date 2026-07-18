"""
Executive Summary Generator

Generates a business summary for executives.
"""

from src.analytics.market_pulse import PulseResult


class ExecutiveSummaryEngine:

    def generate(self, pulse: PulseResult):

        lines = []

        lines.append(
            f"{pulse.total_events} business events were detected."
        )

        lines.append(
            f"The dominant activity is {pulse.dominant_event.lower()}."
        )

        if pulse.funding == "Strong":

            lines.append(
                "Investment activity remains very healthy."
            )

        if pulse.hiring == "Strong":

            lines.append(
                "Hiring demand continues to grow."
            )

        if pulse.layoffs == "Strong":

            lines.append(
                "Layoff activity should be monitored closely."
            )

        if pulse.expansion in ("Strong", "Moderate"):

            lines.append(
                "Expansion activity indicates market optimism."
            )

        return "\n".join(lines)