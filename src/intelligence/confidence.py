"""
Confidence Engine

Computes explainable confidence scores for business events.
"""


class ConfidenceScorer:
    def __init__(self):

        self.WEIGHTS = {
            "company": 0.25,
            "amount": 0.25,
            "publisher": 0.15,
            "keyword": 0.20,
            "round": 0.10,
            "article": 0.05,
        }

        self.TRUSTED_PUBLISHERS = {
            "CNBC",
            "TechCrunch",
            "Reuters",
            "Bloomberg",
            "Economic Times",
            "Entrackr",
            "YourStory",
            "Moneycontrol",
            "Business Standard",
            "Inc42",
            "Indian Startup Times",
        }

    def funding(self, company, amount, funding_round, article_type, source=None):

        score = 0.0

        evidence = []

        # --------------------------------------

        # Company

        # --------------------------------------

        if company:
            score += self.WEIGHTS["company"]

            evidence.append(f"Company detected: {company}")

        # --------------------------------------

        # Money

        # --------------------------------------

        if amount:
            score += self.WEIGHTS["amount"]

            evidence.append("Funding amount detected")

        # --------------------------------------

        # Funding Round

        # --------------------------------------

        if funding_round:
            score += self.WEIGHTS["round"]

            evidence.append(f"Funding round detected: {funding_round}")

        # --------------------------------------

        # Publisher

        # --------------------------------------

        if source in self.TRUSTED_PUBLISHERS:
            score += self.WEIGHTS["publisher"]

            evidence.append(f"Trusted publisher: {source}")

        # --------------------------------------

        # Keywords

        # --------------------------------------

        score += self.WEIGHTS["keyword"]

        evidence.append("Funding keywords detected")

        # --------------------------------------

        # Article Type

        # --------------------------------------

        if article_type == "Company Event":
            score += self.WEIGHTS["article"]

            evidence.append("Company event classified")

        elif article_type == "Market Summary":
            evidence.append("Market summary classified")

        else:
            evidence.append("General article classified")

        score = round(min(score, 1.0), 2)

        return score, evidence

    def hiring(self, company, article_type, source=None):

        score = 0.4

        evidence = []

        if company:
            score += 0.3

            evidence.append(f"Company detected: {company}")

        if source in self.TRUSTED_PUBLISHERS:
            score += 0.2

            evidence.append(f"Trusted publisher: {source}")

        if article_type == "Company Event":
            score += 0.1

            evidence.append("Company hiring event")

        return round(min(score, 1.0), 2), evidence

    def layoff(self, company, article_type, source=None):

        score = 0.4

        evidence = []

        if company:
            score += 0.3

            evidence.append(f"Company detected: {company}")

        if source in self.TRUSTED_PUBLISHERS:
            score += 0.2

            evidence.append(f"Trusted publisher: {source}")

        if article_type == "Company Event":
            score += 0.1

            evidence.append("Company layoff event")

        return round(min(score, 1.0), 2), evidence
