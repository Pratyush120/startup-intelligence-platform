"""
Regex Patterns
"""

import re

MONEY_PATTERN = re.compile(
    r"""
    (?:
        (\$|₹|USD|INR|Rs\.?|Rs)
        \s*
    )?

    ([\d,.]+)

    \s*

    (
        million|
        billion|
        m|
        b|
        crore|
        cr|
        lakh|
        lakhs
    )?

    """,
    re.IGNORECASE | re.VERBOSE,
)

PERCENT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)%")
