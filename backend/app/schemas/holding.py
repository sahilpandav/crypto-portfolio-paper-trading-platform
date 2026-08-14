from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class HoldingResponse(BaseModel):
    id: int
    coin_symbol: str
    quantity: Decimal
    average_buy_price: Decimal
    current_price: Decimal
    current_value: Decimal
    profit_loss: Decimal
    profit_loss_percent: Decimal
    updated_at: datetime

    class Config:
        from_attributes = True