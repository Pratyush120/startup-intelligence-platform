import re

from src.models.events.funding_event import FundingEvent


class FundingExtractor:
    def __init__(self):

        self.money_pattern = re.compile(
            r"(\$|₹|USD|INR)\s*([\d,.]+)\s*(million|billion|M|B|Cr|Crore|Lakh)?",
            re.IGNORECASE,
        )

        self.round_pattern = re.compile(
            r"(Pre[- ]?Seed|Seed|Angel|Series A|Series B|Series C|Series D|Series E|IPO)",
            re.IGNORECASE,
        )

    def extract(self, title, description):

        text = f"{title} {description}"

        money = self.money_pattern.search(text)

        round_match = self.round_pattern.search(text)

        amount = None
        currency = None

        confidence = 0.0

        if money:
            currency = money.group(1)

            number = money.group(2)

            scale = money.group(3)

            amount = f"{number} {scale}" if scale else number

            confidence += 0.5

        funding_round = None

        if round_match:
            funding_round = round_match.group(1)

            confidence += 0.3

        if money and "fund" in text.lower():
            confidence += 0.2

        return FundingEvent(
            company=None,
            amount=amount,
            currency=currency,
            round=funding_round,
            source_article=title,
            confidence=round(confidence, 2),
        )
