from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Article:

    title: str

    body: str

    canonical_url: str

    publisher: str

    authors: List[str]

    publish_date: Optional[str]

    keywords: List[str]

    summary: str

    top_image: Optional[str]

    language: Optional[str]