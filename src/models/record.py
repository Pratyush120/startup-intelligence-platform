"""
Unified Record Model

Every collector in the platform must return this schema.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Record:
    source: str

    title: str

    description: str

    url: str

    published_at: Optional[str]

    collected_at: str

    record_type: str

    metadata: Dict = field(default_factory=dict)
