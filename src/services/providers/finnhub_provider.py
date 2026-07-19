import os
import httpx
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from src.utils.logger import get_logger
from src.models.intelligence import FinancialMetric, SourceAttribution

logger = get_logger(__name__)

class FinnhubProvider:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")
        if not self.api_key:
            logger.warning("FINNHUB_API_KEY is missing. Finnhub provider will degrade gracefully.")
        self.base_url = "https://finnhub.io/api/v1"

    async def _resolve_ticker(self, company_name: str, client: httpx.AsyncClient) -> Optional[str]:
        # Naive resolution using Finnhub search endpoint
        try:
            response = await client.get(
                f"{self.base_url}/search",
                params={"q": company_name, "token": self.api_key}
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("result", [])
            if results:
                # Prefer Common Stock
                for r in results:
                    if r.get("type") == "Common Stock":
                        return r.get("symbol")
                return results[0].get("symbol")
        except Exception as e:
            logger.debug(f"Finnhub ticker resolution failed for '{company_name}': {e}")
        return None

    async def fetch_financials(self, company_name: str) -> List[FinancialMetric]:
        if not self.api_key:
            return []
            
        metrics = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                ticker = await self._resolve_ticker(company_name, client)
                if not ticker:
                    return []
                
                response = await client.get(
                    f"{self.base_url}/quote",
                    params={"symbol": ticker, "token": self.api_key}
                )
                response.raise_for_status()
                data = response.json()
                
                attribution = SourceAttribution(
                    provider="Finnhub",
                    url=f"https://finnhub.io",
                    retrieved_at=datetime.now(timezone.utc).isoformat(),
                    confidence=1.0,
                    provider_id=ticker
                )
                
                if "c" in data and data["c"]:
                    metrics.append(FinancialMetric(
                        metric_name="Current Price",
                        value=float(data["c"]),
                        source=attribution
                    ))
                if "pc" in data and data["pc"]:
                    metrics.append(FinancialMetric(
                        metric_name="Previous Close",
                        value=float(data["pc"]),
                        source=attribution
                    ))
        except Exception as e:
            logger.error(f"Finnhub financial request failed: {e}")
            
        return metrics
