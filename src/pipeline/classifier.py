"""
Classification Engine

Classifies startup intelligence records into 18 distinct categories based on heuristics and keywords.
"""

import re
from typing import List, Tuple

from src.models.record import Record
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Categories defined by the architecture
CATEGORIES = [
    "Funding",
    "Hiring",
    "Layoffs",
    "Acquisition",
    "IPO",
    "Product Launch",
    "Partnership",
    "Expansion",
    "Regulation",
    "Leadership",
    "Security",
    "Market Trend",
    "AI",
    "Healthcare",
    "Fintech",
    "Climate",
    "Consumer",
    "Enterprise",
]

# Keywords mapping for simple heuristic classification
KEYWORD_MAP = {
    "Funding": [
        r"\bfund(ing|s)?\b",
        r"\braise(s|d)?\b",
        r"\bseries [a-z]\b",
        r"\bseed\b",
        r"\bcapital\b",
        r"\bventure\b",
    ],
    "Hiring": [
        r"\bhir(e|ing)\b",
        r"\brecruit(ing|ment)?\b",
        r"\bteam expansion\b",
        r"\btalent\b",
    ],
    "Layoffs": [
        r"\blayoffs?\b",
        r"\bfir(e|ing)\b",
        r"\bcut(s|ting)? jobs\b",
        r"\brestructur(e|ing)\b",
        r"\bdownsizing\b",
    ],
    "Acquisition": [
        r"\bacquir(e|es|ed|ing)\b",
        r"\bacquisition\b",
        r"\bmerg(e|er|ing)\b",
        r"\bbuyout\b",
        r"\bbuys\b",
    ],
    "IPO": [
        r"\bipo\b",
        r"\binitial public offering\b",
        r"\bgo(ing)? public\b",
        r"\bspac\b",
    ],
    "Product Launch": [
        r"\blaunch(ed|es|ing)?\b",
        r"\bnew product\b",
        r"\breleas(e|ed|es)\b",
        r"\bbeta\b",
        r"\brollout\b",
    ],
    "Partnership": [
        r"\bpartner(s|ship)?\b",
        r"\balliance\b",
        r"\bcollaboration\b",
        r"\bteam(s)? up\b",
        r"\bjoin(s)? forces\b",
    ],
    "Expansion": [
        r"\bexpan(d|sion)\b",
        r"\bnew market(s)?\b",
        r"\bglobal\b",
        r"\bopen(s)? office\b",
    ],
    "Regulation": [
        r"\bregulat(ion|ory)\b",
        r"\bcompliance\b",
        r"\bsec\b",
        r"\bfcc\b",
        r"\blawsuit\b",
        r"\bsue(s|d)?\b",
    ],
    "Leadership": [
        r"\bceo\b",
        r"\bcto\b",
        r"\bexecutive(s)?\b",
        r"\bboard of directors\b",
        r"\bstep(s)? down\b",
        r"\bappoint(s|ed)\b",
    ],
    "Security": [
        r"\bhack(ed|er)?\b",
        r"\bbreach\b",
        r"\bcybersecurity\b",
        r"\bvulnerability\b",
        r"\bdata leak\b",
    ],
    "Market Trend": [
        r"\btrend(s)?\b",
        r"\bmarket report\b",
        r"\banalysis\b",
        r"\bforecast\b",
        r"\boutlook\b",
    ],
    "AI": [
        r"\bai\b",
        r"\bartificial intelligence\b",
        r"\bllm\b",
        r"\bmachine learning\b",
        r"\bgenerative\b",
        r"\bchatgpt\b",
    ],
    "Healthcare": [
        r"\bhealth(care|tech)?\b",
        r"\bmedical\b",
        r"\bpharma\b",
        r"\bbiotech\b",
        r"\bpatients?\b",
    ],
    "Fintech": [
        r"\bfintech\b",
        r"\bpayment(s)?\b",
        r"\bcrypto(currency)?\b",
        r"\bdefi\b",
        r"\bblock(chain)?\b",
        r"\bbanking\b",
    ],
    "Climate": [
        r"\bclimate(tech)?\b",
        r"\bsustainab(le|ility)\b",
        r"\bgreen\b",
        r"\bcarbon\b",
        r"\brenewable\b",
        r"\bclean( )?energy\b",
    ],
    "Consumer": [r"\bconsumer(s)?\b", r"\bd2c\b", r"\bretail\b", r"\be(-)?commerce\b"],
    "Enterprise": [
        r"\benterprise(s)?\b",
        r"\bb2b\b",
        r"\bsaas\b",
        r"\bcorporate\b",
        r"\bbusiness software\b",
    ],
}


class Classifier:
    def classify(self, records: List[Record]) -> List[Record]:
        logger.info(f"Classifying {len(records)} records")

        for record in records:
            category, confidence = self._predict_category(record)
            # Store it in metadata since Record doesn't strictly have a 'category' attribute by default
            # Actually, let's see if we should set 'record_type' or put it in metadata.
            # We'll put it in metadata as requested by orchestrator expectations.
            record.metadata["category"] = category
            record.metadata["confidence"] = confidence

            # If the record type is still 'news', we might want to keep it or update it.
            # We will keep record.record_type = "news" to match existing code, and use metadata for classification.

        return records

    def _predict_category(self, record: Record) -> Tuple[str, float]:
        text = f"{record.title} {record.description}".lower()

        scores = {cat: 0.0 for cat in CATEGORIES}

        for category, patterns in KEYWORD_MAP.items():
            for pattern in patterns:
                # Add 0.3 for every match to build confidence
                matches = len(re.findall(pattern, text))
                if matches > 0:
                    scores[category] += 0.3 + (matches * 0.1)

                    # Boost if found in title
                    if len(re.findall(pattern, record.title.lower())) > 0:
                        scores[category] += 0.2

        # Get highest scoring category
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        if best_score == 0.0:
            return "Market Trend", 0.5  # Fallback category

        # Cap confidence at 0.95 for heuristics
        confidence = min(0.95, 0.4 + best_score)

        return best_category, round(confidence, 2)
