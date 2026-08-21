from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class WatchlistCreate(BaseModel):
    coin_symbol: str = Field(min_length=1, max_length=20)


class WatchlistResponse(BaseModel):
    id: int
    coin_symbol: str
    current_price: Decimal
    price_change_percent_24h: Decimal
    created_at: datetime

    class Config:
        from_attributes = True