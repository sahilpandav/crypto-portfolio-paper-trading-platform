from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class WalletResponse(BaseModel):
    id: int
    balance: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True