from decimal import Decimal

import httpx
from fastapi import HTTPException, status

from app.core.config import settings


def get_current_price(coin_symbol: str) -> Decimal:
    pair = f"{coin_symbol.upper()}USDT"

    try:
        response = httpx.get(
            f"{settings.binance_api_base_url}/api/v3/ticker/price",
            params={"symbol": pair},
            timeout=5.0,
        )
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not fetch live price for {coin_symbol}.",
        )

    data = response.json()
    return Decimal(data["price"])