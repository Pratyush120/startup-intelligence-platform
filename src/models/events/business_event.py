"""
Universal Business Event Model

Every interpreter produces one or more BusinessEvent objects.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BusinessEvent:
    """
    Standard business intelligence event.

    Every event produced by the Intelligence Engine
    follows this schema regardless of source.
    """

    # --------------------------------------------------
    # Core Event Information
    # --------------------------------------------------

    event_type: str

    article_type: str = "General"

    company: Optional[str] = None

    title: str = ""

    source: str = ""

    published_at: Optional[str] = None

    # --------------------------------------------------
    # Intelligence Scores
    # --------------------------------------------------

    confidence: float = 0.0

    impact_score: float = 0.0

    # --------------------------------------------------
    # Extracted Structured Data
    # --------------------------------------------------

    entities: Dict[str, Any] = field(default_factory=dict)

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    evidence: List[str] = field(default_factory=list)

    reasoning: str = ""

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    tags: List[str] = field(default_factory=list)

    # --------------------------------------------------
    # Future Analytics
    # --------------------------------------------------

    metadata: Dict[str, Any] = field(default_factory=dict)

    # --------------------------------------------------
    # Helper Methods
    # --------------------------------------------------

    def add_tag(self, tag: str):

        if tag not in self.tags:
            self.tags.append(tag)

    def add_evidence(self, item: str):

        self.evidence.append(item)

    def add_entity(self, key: str, value: Any):

        self.entities[key] = value

    def to_dict(self):

        return {

            "event_type": self.event_type,

            "article_type": self.article_type,

            "company": self.company,

            "title": self.title,

            "source": self.source,

            "published_at": self.published_at,

            "confidence": self.confidence,

            "impact_score": self.impact_score,

            "entities": self.entities,

            "evidence": self.evidence,

            "reasoning": self.reasoning,

            "tags": self.tags,

            "metadata": self.metadata,

        }

    def __str__(self):

        return (

            f"{self.event_type}"

            f" | {self.company}"

            f" | {self.title}"

        )