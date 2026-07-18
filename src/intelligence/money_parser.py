"""
Money Parser V3

Extracts and normalizes monetary values.
"""

import re


class MoneyParser:

    PATTERN = re.compile(
        r"""
        (?P<currency>\$|₹|USD|INR|Rs\.?)?
        \s*
        (?P<amount>\d+(?:\.\d+)?)
        \s*
        (?P<unit>
            billion|
            million|
            crore|
            cr|
            lakh|
            lakhs|
            bn|
            mn|
            b|
            m
        )?
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    MULTIPLIERS = {

        "billion": 1_000_000_000,
        "bn": 1_000_000_000,
        "b": 1_000_000_000,

        "million": 1_000_000,
        "mn": 1_000_000,
        "m": 1_000_000,

        "crore": 10_000_000,
        "cr": 10_000_000,

        "lakh": 100_000,
        "lakhs": 100_000

    }

    def parse(self, text):

        match = self.PATTERN.search(text)

        if not match:
            return None

        currency = match.group("currency")
        amount = float(match.group("amount"))
        unit = match.group("unit")

        multiplier = 1

        if unit:
            multiplier = self.MULTIPLIERS.get(
                unit.lower(),
                1
            )

        normalized = amount * multiplier

        if currency in ["$", "USD"]:
            currency = "USD"

        elif currency in ["₹", "Rs", "Rs.", "INR"]:
            currency = "INR"

        return {

            "raw": match.group(0).strip(),

            "currency": currency,

            "display_amount": f"{amount:g} {unit}" if unit else f"{amount:g}",

            "amount": int(normalized),

            "unit": unit

        }