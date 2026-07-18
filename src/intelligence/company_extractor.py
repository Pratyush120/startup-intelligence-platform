"""
Company Extraction Engine V3

Rule-based extraction for startup news headlines.
"""

import re

from src.company.company_dictionary import KNOWN_COMPANIES
from src.company.company_resolver import CompanyResolver


class CompanyExtractor:

    def __init__(self):

        self.resolver = CompanyResolver()

        self.stopwords = {

            # Months
            "January","February","March","April","May","June","July",
            "August","September","October","November","December",

            # News Words
            "The","These","This","That","How","Why","What",
            "Between","After","Before","During","Against","Over",

            # Startup Words
            "Startup","Startups","Indian","India",

            "Funding","Fund","Fundraise","Fundraising",
            "Investment","Investments",
            "Investor","Investors",

            "Raise","Raises","Raised",

            "Series","Bridge","Round",

            "Technology","Technologies",
            "Platform",
            "Assistant",
            "Business",
            "Commerce",
            "Infrastructure",

            "AI","ML",

            # Money
            "Million","Billion","Mn","M","Cr","Crore",
            "Lakh","Lakhs","USD","INR","Rs"

        }

    def clean_token(self, token):

        token = token.strip()

        token = token.replace("'s", "")

        token = token.replace(",", "")

        token = token.replace(".", "")

        return token

    def tokenize(self, title):

        return re.findall(

            r"[A-Z][A-Za-z0-9&.'-]*",

            title

        )

    def extract(self, title):

        tokens = [

            self.clean_token(t)

            for t in self.tokenize(title)

        ]

        # -----------------------------
        # STEP 1
        # Direct dictionary lookup
        # -----------------------------

        title_lower = title.lower()

        for company in KNOWN_COMPANIES:

            if company.lower() in title_lower:

                return company

        # -----------------------------
        # STEP 2
        # Candidate extraction
        # -----------------------------

        candidates = []

        for token in tokens:

            if len(token) < 2:
                continue

            if token.isdigit():
                continue

            if token in self.stopwords:
                continue

            if re.fullmatch(r"\d+", token):
                continue

            candidates.append(token)

        # -----------------------------
        # STEP 3
        # Alias resolution
        # -----------------------------

        for candidate in candidates:

            resolved = self.resolver.resolve(candidate)

            if resolved is not None :

                return resolved



        return None