"""
Funding Interpreter

Converts funding-related news into BusinessEvent objects.
"""

from src.intelligence.base_interpreter import BaseInterpreter
from src.models.events.business_event import BusinessEvent

from src.intelligence.company_extractor import CompanyExtractor
from src.intelligence.money_parser import MoneyParser
from src.intelligence.article_classifier import ArticleClassifier
from src.intelligence.confidence import ConfidenceScorer
from src.intelligence.impact import ImpactScorer

from src.knowledge.constants import (
    FUNDING_KEYWORDS,
    FUNDING_ROUNDS,
)


class FundingInterpreter(BaseInterpreter):
    def __init__(self):

        self.company_extractor = CompanyExtractor()

        self.money_parser = MoneyParser()

        self.article_classifier = ArticleClassifier()

        self.confidence = ConfidenceScorer()

        self.impact = ImpactScorer()

    # -----------------------------------------------------

    def is_funding_article(self, text):

        text = text.lower()

        return any(keyword.lower() in text for keyword in FUNDING_KEYWORDS)

    # -----------------------------------------------------

    def detect_round(self, text):

        text = text.lower()

        for funding_round in FUNDING_ROUNDS:
            if funding_round.lower() in text:
                return funding_round

        return None

    # -----------------------------------------------------

    def interpret(self, record):

        text = f"{record.title} {record.description}"

        # ----------------------------------------------
        # Ignore non funding articles
        # ----------------------------------------------

        if not self.is_funding_article(text):
            return []

        # ----------------------------------------------
        # Article Classification
        # ----------------------------------------------

        article_type = self.article_classifier.classify(record.title)

        # ----------------------------------------------
        # Company Extraction
        # ----------------------------------------------

        company = None

        if article_type == "Company Event":
            company = self.company_extractor.extract(record.title)

        # ----------------------------------------------
        # Money Parsing
        # ----------------------------------------------

        money = self.money_parser.parse(text)

        amount = None
        currency = None
        unit = None
        display_amount = None
        raw_amount = None

        if money:
            amount = money["amount"]

            currency = money["currency"]

            unit = money["unit"]

            display_amount = money["display_amount"]

            raw_amount = money["raw"]

        # ----------------------------------------------
        # Funding Round
        # ----------------------------------------------

        funding_round = self.detect_round(text)

        # ----------------------------------------------
        # Confidence
        # ----------------------------------------------

        confidence, evidence = self.confidence.funding(
            company=company,
            amount=amount,
            funding_round=funding_round,
            article_type=article_type,
            source=record.source,
        )

        # ----------------------------------------------
        # Impact
        # ----------------------------------------------

        impact_score = self.impact.funding(funding_round=funding_round, unit=unit)

        # ----------------------------------------------
        # Build Event
        # ----------------------------------------------

        event = BusinessEvent(
            event_type="Funding",
            article_type=article_type,
            company=company,
            title=record.title,
            source=record.source,
            published_at=record.published_at,
            confidence=confidence,
            impact_score=impact_score,
            entities={
                "amount": amount,
                "display_amount": display_amount,
                "raw_amount": raw_amount,
                "currency": currency,
                "unit": unit,
                "round": funding_round,
            },
            evidence=evidence,
            reasoning=(
                "Funding event detected using "
                "article classification, "
                "company extraction, "
                "money parsing, "
                "funding round detection "
                "and confidence scoring."
            ),
            tags=["funding", "investment"],
        )

        return [event]
