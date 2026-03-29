from pydantic import BaseModel, Field


class TradeRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    side: str = Field(pattern="^(buy|sell)$")
    order_type: str = Field(pattern="^(market|limit)$")
    quantity: float = Field(gt=0)
    limit_price: float | None = Field(default=None, gt=0)


class TradeResponse(BaseModel):
    order_id: str
    status: str
    broker: str
    ticker: str
    side: str
    order_type: str
    quantity: float
    limit_price: float | None = None
    submitted_at: str
