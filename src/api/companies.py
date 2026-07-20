from fastapi import APIRouter, Depends, Query
from typing import Any, List, Optional
from src.api.response import StandardResponse, success_response, error_response
from src.api.deps import get_repository
from src.database.repository import Repository
from src.pipeline.api_serializer import serialize_company_metrics

router = APIRouter(tags=["Companies"])


class CompanyProxy:
    """Helper to mock object attributes for serializer compatibility."""

    def __init__(self, data: dict):
        for k, v in data.items():
            setattr(self, k, v)


@router.get("/companies", response_model=StandardResponse[List[dict[str, Any]]])
async def get_companies(
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sector: Optional[str] = None,
    repo: Repository = Depends(get_repository),
):
    companies = repo.get_top_companies(limit=limit, offset=offset, sector=sector)

    # We need to build sparklines and proxy objects for serializer
    company_proxies = []
    sparklines = {}
    for c in companies:
        c_name = c["company_name"]
        company_proxies.append(CompanyProxy(c))
        history = repo.get_company_history(c_name)
        if not history:
            history = [c.get("business_health", 50.0)]
        # Simple placeholder for sparkline generation without re-running SparklineGenerator
        # In a fully integrated system we'd use SparklineGenerator.generate(history)
        # But we can just use the history directly for the API if it's 5 points
        if len(history) < 5:
            history = history + [history[-1]] * (5 - len(history))
        sparklines[c_name] = history[-5:]

    serialized = serialize_company_metrics(company_proxies, sparklines)
    return success_response(
        data=serialized,
        meta={
            "limit": limit,
            "offset": offset,
            "sector": sector,
            "total": len(serialized),
        },
    )


@router.get("/company/{id}", response_model=StandardResponse[dict[str, Any]])
async def get_company(id: str, repo: Repository = Depends(get_repository)):
    clean_id = id.replace("c_", "").replace("_", " ")

    from src.services.intelligence_aggregator import IntelligenceAggregator

    aggregator = IntelligenceAggregator(repo)
    profile = await aggregator.build_company_intelligence(clean_id)

    if not profile or not profile.company_name:
        return error_response(["Company not found."])

    # Convert normalized profile back into legacy DB format so we can use existing frontend serializers
    # In a full migration, the frontend would directly consume Pydantic CompanyProfile
    c_dict = {
        "company_name": profile.company_name,
        "website": profile.website,
        "sector": profile.description,
        "business_health": 85.0,  # Mock since we'd need to extract from profile
        "momentum_score": 90.0,
    }

    history = repo.get_company_history(profile.company_name)
    if not history:
        history = [85.0]
    if len(history) < 5:
        history = history + [history[-1]] * (5 - len(history))

    serialized = serialize_company_metrics(
        [CompanyProxy(c_dict)], {profile.company_name: history[-5:]}
    )

    # Inject live financials and news into the final dict
    resp_data = serialized[0]
    resp_data["liveFinancials"] = [f.model_dump() for f in profile.financials]

    return success_response(data=resp_data)
