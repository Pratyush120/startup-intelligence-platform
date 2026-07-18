from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:

    company_name: str

    canonical_name: Optional[str] = None

    sector: Optional[str] = None

    country: Optional[str] = None

    city: Optional[str] = None

    website: Optional[str] = None

    linkedin: Optional[str] = None

    startup_india_id: Optional[str] = None
    