from fastapi import APIRouter, HTTPException

from app.models.financials import CompanyResearchResponse
from app.services.research_service import get_company_research
from app.services.sec_edgar import EdgarUnavailableError, TickerNotFoundError

router = APIRouter(prefix="/research", tags=["research"])


@router.get("/{ticker}", response_model=CompanyResearchResponse)
def get_research(ticker: str) -> CompanyResearchResponse:
    try:
        return get_company_research(ticker)
    except TickerNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"No SEC registrant found for ticker {ticker.upper().strip()!r}.",
        ) from None
    except EdgarUnavailableError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
