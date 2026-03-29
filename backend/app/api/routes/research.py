from fastapi import APIRouter

from app.models.financials import CompanyResearchResponse
from app.services.research_service import get_company_research

router = APIRouter(prefix="/research", tags=["research"])


@router.get("/{ticker}", response_model=CompanyResearchResponse)
def get_research(ticker: str) -> CompanyResearchResponse:
    return get_company_research(ticker)
