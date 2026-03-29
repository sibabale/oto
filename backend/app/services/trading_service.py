from datetime import UTC, datetime
from uuid import uuid4

from app.models.trades import TradeRequest, TradeResponse


class TradeValidationError(ValueError):
    """Raised when an order payload fails domain-level validation."""


def place_trade(order: TradeRequest) -> TradeResponse:
    if order.order_type == "limit" and order.limit_price is None:
        raise TradeValidationError("limit_price is required for limit orders")

    order_id = f"paper-{uuid4().hex[:12]}"

    return TradeResponse(
        order_id=order_id,
        status="accepted",
        broker="paper",
        ticker=order.ticker.upper(),
        side=order.side,
        order_type=order.order_type,
        quantity=order.quantity,
        limit_price=order.limit_price,
        submitted_at=datetime.now(UTC).isoformat(),
    )
