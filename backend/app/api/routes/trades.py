from fastapi import APIRouter, HTTPException, status

from app.models.trades import TradeRequest, TradeResponse
from app.services.trading_service import TradeValidationError, place_trade

router = APIRouter(prefix="/trades", tags=["trades"])


@router.post("", response_model=TradeResponse, status_code=status.HTTP_201_CREATED)
def create_trade(payload: TradeRequest) -> TradeResponse:
    try:
        return place_trade(payload)
    except TradeValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "TRADE_VALIDATION_ERROR",
                "message": str(exc),
            },
        ) from exc
