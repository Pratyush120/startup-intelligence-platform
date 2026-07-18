"""
Hiring Interpreter
"""

import re

from src.intelligence.base_interpreter import BaseInterpreter
from src.models.events.business_event import BusinessEvent


HIRING_KEYWORDS = [
    "hire",
    "hiring",
    "recruit",
    "recruiting",
    "jobs",
    "workforce",
    "expand team"
]

NUMBER_PATTERN = re.compile(r"\b(\d{2,5})\b")


class HiringInterpreter(BaseInterpreter):

    def interpret(self, record):

        text = f"{record.title} {record.description}"

        lower_text = text.lower()

        if not any(keyword in lower_text for keyword in HIRING_KEYWORDS):
            return []

        hires = None

        match = NUMBER_PATTERN.search(text)

        if match:

            hires = int(match.group(1))

        confidence = 0.8

        if hires:

            confidence = 0.95

        event = BusinessEvent(

            event_type="Hiring",

            company=None,

            title=record.title,

            source=record.source,

            published_at=record.published_at,

            confidence=confidence,

            impact_score=min((hires or 50) / 10, 100),

            entities={

                "estimated_hires": hires

            },

            evidence=[

                "Hiring keyword detected"

            ],

            reasoning="Rule-based hiring detection.",

            tags=[

                "hiring"

            ]

        )

        return [event]