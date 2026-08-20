from decimal import Decimal

from pydantic import BaseModel


class CoinTicker(BaseModel):
    symbol: str
    price: Decimal
    price_change_percent_24h: Decimal
    high_24h: Decimal
    low_24h: Decimal
    volume_24h: Decimal