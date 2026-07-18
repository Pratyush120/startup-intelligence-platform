"""
Business scoring engine.
"""

ROUND_SCORE = {
    "Pre-Seed": 15,
    "Seed": 25,
    "Angel": 20,
    "Series A": 45,
    "Series B": 60,
    "Series C": 75,
    "Series D": 85,
    "Series E": 90,
    "Series F": 95,
    "IPO": 100
}


def funding_impact(round_name):

    if round_name is None:
        return 30

    return ROUND_SCORE.get(round_name, 30)