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


def get_market_overview(limit: int = 20) -> list[dict]:
    try:
        response = httpx.get(
            f"{settings.binance_api_base_url}/api/v3/ticker/24hr",
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not fetch market data.",
        )

    all_tickers = response.json()

    usdt_pairs = [t for t in all_tickers if t["symbol"].endswith("USDT")]
    usdt_pairs.sort(key=lambda t: Decimal(t["quoteVolume"]), reverse=True)

    return usdt_pairs[:limit]


def get_coin_ticker(coin_symbol: str) -> dict:
    pair = f"{coin_symbol.upper()}USDT"

    try:
        response = httpx.get(
            f"{settings.binance_api_base_url}/api/v3/ticker/24hr",
            params={"symbol": pair},
            timeout=5.0,
        )
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coin '{coin_symbol}' not found.",
        )

    return response.json()