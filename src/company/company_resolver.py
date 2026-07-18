"""
Company Resolver

Resolves extracted company names and filters out
non-primary organizations.
"""

from rapidfuzz import process

from src.company.aliases import ALIASES
from src.company.company_dictionary import (
    COMPANIES,
    KNOWN_COMPANIES,
)


class CompanyResolver:
    def resolve(self, company_name):

        if not company_name:
            return None

        company_name = company_name.strip()

        # -------------------------
        # Alias
        # -------------------------

        alias = ALIASES.get(company_name.lower())

        if alias:
            company_name = alias

        # -------------------------
        # Fuzzy Match
        # -------------------------

        match = process.extractOne(company_name, KNOWN_COMPANIES, score_cutoff=88)

        if not match:
            return company_name

        company = match[0]

        info = COMPANIES.get(company)

        if not info:
            return company

        company_type = info["type"]

        # Ignore non-primary organizations

        if company_type in {"vc", "law_firm"}:
            return None

        return company
