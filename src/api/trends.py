from fastapi import APIRouter, Depends
from typing import Any, List
from src.api.response import StandardResponse, success_response
from src.api.deps import get_repository
from src.database.repository import Repository

router = APIRouter(tags=["Trends"])

@router.get("/trends", response_model=StandardResponse[List[dict[str, Any]]])
async def get_trends(repo: Repository = Depends(get_repository)):
    # Calculate macro trends from DB or return mocks
    # This was previously mocked in the frontend
    
    # We can calculate simple sector momentum
    repo.db.execute(
        "SELECT sector, AVG(momentum_score) as avg_momentum, COUNT(company_id) as entity_count FROM companies WHERE sector IS NOT NULL GROUP BY sector ORDER BY avg_momentum DESC LIMIT 5"
    )
    rows = repo.db.fetchall()
    
    trends = []
    for idx, r in enumerate(rows):
        trends.append({
            "id": f"t_{idx}",
            "name": f"{r['sector']} Momentum",
            "velocity": round(r["avg_momentum"], 1),
            "sector": r["sector"],
            "topEntityIds": []
        })
        
    if not trends:
        # Fallback if no companies are categorized
        trends = [
            {
                "id": "t_fallback",
                "name": "AI Infrastructure",
                "velocity": 14.5,
                "sector": "AI",
                "topEntityIds": []
            }
        ]
        
    return success_response(data=trends)
