"""
Company Dictionary

Maps organization names to their roles.
"""

COMPANIES = {

    # -----------------------
    # Startups
    # -----------------------

    "Rapido": {"type": "startup"},
    "Razorpay": {"type": "startup"},
    "PhonePe": {"type": "startup"},
    "Zepto": {"type": "startup"},
    "Zave": {"type": "startup"},
    "Groww": {"type": "startup"},
    "CRED": {"type": "startup"},
    "Meesho": {"type": "startup"},
    "Swiggy": {"type": "startup"},
    "Zomato": {"type": "startup"},
    "Nykaa": {"type": "startup"},
    "Paytm": {"type": "startup"},
    "Flipkart": {"type": "startup"},
    "Bodycraft": {"type": "startup"},
    "Alienkind": {"type": "startup"},
    "Finnovate": {"type": "startup"},
    "SaffronStays": {"type": "startup"},
    "JustAI": {"type": "startup"},

    # -----------------------
    # Big Tech
    # -----------------------

    "Amazon": {"type": "company"},
    "Google": {"type": "company"},
    "Microsoft": {"type": "company"},
    "Meta": {"type": "company"},
    "Apple": {"type": "company"},
    "OpenAI": {"type": "company"},

    # -----------------------
    # Venture Capital
    # -----------------------

    "Lightspeed": {"type": "vc"},
    "Sequoia": {"type": "vc"},
    "Peak XV": {"type": "vc"},
    "Peak XV Partners": {"type": "vc"},
    "Accel": {"type": "vc"},
    "General Catalyst": {"type": "vc"},
    "Matrix": {"type": "vc"},
    "Kalaari": {"type": "vc"},
    "Blume Ventures": {"type": "vc"},
    "Elevation Capital": {"type": "vc"},
    "Inflection Point Ventures": {"type": "vc"},

    # -----------------------
    # Advisors
    # -----------------------

    "Trilegal": {"type": "law_firm"},
    "CAM": {"type": "law_firm"},
    "TT&A": {"type": "law_firm"},
}

KNOWN_COMPANIES = list(COMPANIES.keys())