from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.trade import TradeType


class TradeRequest(BaseModel):
    coin_symbol: str = Field(min_length=1, max_length=20)
    quantity: Decimal = Field(gt=0)


class TradeResponse(BaseModel):
    id: int
    coin_symbol: str
    trade_type: TradeType
    quantity: Decimal
    price_at_trade: Decimal
    total_value: Decimal
    created_at: datetime

    class Config:
        from_attributes = True