"""
Article Classifier

Determines whether an article is:

1. Company Event
2. Market Summary
3. Industry Report
4. General News

This prevents assigning fake companies to ecosystem-wide articles.
"""

import re


class ArticleClassifier:
    def __init__(self):

        self.market_summary_patterns = [
            r"startup funding",
            r"indian startups",
            r"startup ecosystem",
            r"ecosystem",
            r"funding roundup",
            r"weekly funding",
            r"monthly funding",
            r"funding report",
            r"raised over",
            r"across sectors",
            r"from diverse sectors",
            r"this week",
            r"last week",
            r"top funded startups",
            r"funding landscape",
            r"funding activity",
            r"venture funding",
            r"investment landscape",
        ]

        self.company_event_patterns = [
            r"raises",
            r"raised",
            r"raise",
            r"secures",
            r"secured",
            r"bags",
            r"bagged",
            r"closes",
            r"closed",
            r"announces",
            r"announced",
            r"launches",
            r"launched",
            r"appoints",
            r"appointed",
            r"acquires",
            r"acquired",
            r"hires",
            r"hiring",
            r"opens",
            r"expands",
            r"expansion",
            r"invests",
            r"investment",
            r"fundraise",
            r"fundraising",
        ]

        self.industry_patterns = [
            r"analysis",
            r"report",
            r"survey",
            r"research",
            r"forecast",
            r"market outlook",
            r"industry outlook",
            r"industry report",
        ]

    def classify(self, title: str) -> str:

        title = title.lower()

        # -----------------------------------
        # MARKET SUMMARY
        # -----------------------------------

        for pattern in self.market_summary_patterns:
            if re.search(pattern, title):
                return "Market Summary"

        # -----------------------------------
        # COMPANY EVENT
        # -----------------------------------

        for pattern in self.company_event_patterns:
            if re.search(pattern, title):
                return "Company Event"

        # -----------------------------------
        # INDUSTRY REPORT
        # -----------------------------------

        for pattern in self.industry_patterns:
            if re.search(pattern, title):
                return "Industry Report"

        # -----------------------------------
        # DEFAULT
        # -----------------------------------

        return "General"

    def is_company_event(self, title):

        return self.classify(title) == "Company Event"

    def is_market_summary(self, title):

        return self.classify(title) == "Market Summary"

    def is_industry_report(self, title):

        return self.classify(title) == "Industry Report"
