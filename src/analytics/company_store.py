"""
Company Intelligence Store

Aggregates business events into company profiles.
"""

from src.company.company_profile import CompanyProfile


class CompanyStore:
    def __init__(self):

        self.companies = {}

    def process(self, events):

        for event in events:
            if not event.company:
                continue

            company = event.company

            if company not in self.companies:
                self.companies[company] = CompanyProfile(company)

            self.companies[company].add_event(event)

        for profile in self.companies.values():
            profile.calculate_momentum()

        return self.companies

    def top_companies(self, limit=10):

        return sorted(
            self.companies.values(), key=lambda x: x.momentum_score, reverse=True
        )[:limit]
