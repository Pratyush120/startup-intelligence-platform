from dataclasses import dataclass
from typing import Optional


@dataclass
class FundingEvent:

    company: Optional[str]

    amount: Optional[float]

    currency: Optional[str]

    round: Optional[str]

    source_article: Optional[str]

    confidence: float