import json

from config.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EntityExtractor:
    def __init__(self):

        company_file = Config.BASE_DIR / "config" / "knowledge_base" / "companies.json"

        with open(company_file, "r", encoding="utf-8") as file:
            self.company_catalog = json.load(file)

    def extract_companies(self, text):

        text = text.lower()

        matches = []

        for company in self.company_catalog:
            if company["name"].lower() in text:
                matches.append(company)

                continue

            for alias in company["aliases"]:
                if alias.lower() in text:
                    matches.append(company)

                    break

        logger.info(f"Companies Found : {len(matches)}")

        return matches
