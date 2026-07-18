"""
Company Intelligence Model
"""

from dataclasses import dataclass, field


@dataclass
class CompanyProfile:

    company_name: str

    funding_events: int = 0

    hiring_events: int = 0

    layoff_events: int = 0

    acquisition_events: int = 0

    expansion_events: int = 0

    total_events: int = 0

    latest_funding: int | None = None

    momentum_score: int = 0

    articles: list = field(default_factory=list)

    sources: set = field(default_factory=set)

    def add_event(self, event):

        self.total_events += 1

        self.articles.append(event.title)

        self.sources.add(event.source)

        if event.event_type == "Funding":

            self.funding_events += 1

            amount = event.entities.get("amount")

            if amount:

                self.latest_funding = amount

        elif event.event_type == "Hiring":

            self.hiring_events += 1

        elif event.event_type == "Layoff":

            self.layoff_events += 1

        elif event.event_type == "Expansion":

            self.expansion_events += 1

        elif event.event_type == "Acquisition":

            self.acquisition_events += 1

    def calculate_momentum(self):

        score = 0

        score += self.funding_events * 30

        score += self.hiring_events * 20

        score += self.expansion_events * 25

        score += self.acquisition_events * 35

        score -= self.layoff_events * 25

        self.momentum_score = max(score, 0)