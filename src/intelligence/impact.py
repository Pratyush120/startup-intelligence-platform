"""
Business Impact Scoring
"""


class ImpactScorer:
    ROUND_SCORE = {
        "Pre-Seed": 15,
        "Seed": 25,
        "Angel": 20,
        "Series A": 45,
        "Series B": 60,
        "Series C": 75,
        "Series D": 85,
        "Series E": 90,
        "IPO": 100,
    }

    def funding(self, funding_round, unit):

        score = self.ROUND_SCORE.get(funding_round, 30)

        if unit:
            unit = unit.lower()

            if unit in ["billion", "b"]:
                score += 20

            elif unit in ["million", "m"]:
                score += 10

        return min(score, 100)
