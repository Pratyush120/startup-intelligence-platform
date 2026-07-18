"""
Sparkline Generator

Generates pre-aggregated sparkline arrays for the frontend MetricCard
and TopCompaniesTable components.

The frontend expects a small array of 5 values (0–100 range),
NOT raw historical data — this module performs the aggregation on the backend.
"""

from __future__ import annotations

import statistics
from typing import List

from src.utils.logger import get_logger

logger = get_logger(__name__)


class SparklineGenerator:
    """
    Converts a time-ordered list of momentum scores into a normalized
    5-point sparkline array for the frontend.
    """

    TARGET_POINTS = 5

    def generate(self, history: List[float]) -> List[float]:
        """
        Takes an ordered list of historical momentum scores (any length)
        and returns a 5-point normalized sparkline list.

        Args:
            history: Ordered list of floats (oldest to newest).

        Returns:
            List of 5 floats in the 0-100 range.
        """
        if not history:
            return [50.0] * self.TARGET_POINTS

        if len(history) < self.TARGET_POINTS:
            # Pad with the first value on the left
            history = [history[0]] * (self.TARGET_POINTS - len(history)) + list(history)

        # Sample TARGET_POINTS evenly-spaced values
        indices = [
            int(i * (len(history) - 1) / (self.TARGET_POINTS - 1))
            for i in range(self.TARGET_POINTS)
        ]
        sampled = [history[i] for i in indices]

        # Normalize to 0–100 range based on min/max of the full history
        min_val = min(history)
        max_val = max(history)

        if max_val == min_val:
            return [50.0] * self.TARGET_POINTS

        normalized = [
            round((v - min_val) / (max_val - min_val) * 100, 1)
            for v in sampled
        ]

        return normalized

    def generate_from_event_counts(
        self,
        daily_counts: List[int],
    ) -> List[float]:
        """
        Generates a sparkline from daily event count data.
        Useful for the Market Snapshot MetricCards.
        """
        floats = [float(c) for c in daily_counts]
        return self.generate(floats)
