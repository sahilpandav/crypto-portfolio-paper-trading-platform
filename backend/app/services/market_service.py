from decimal import Decimal

from app.integrations import binance_client
from app.schemas.market import CoinTicker


def _to_coin_ticker(raw_ticker: dict) -> CoinTicker:
    symbol = raw_ticker["symbol"].removesuffix("USDT")

    return CoinTicker(
        symbol=symbol,
        price=Decimal(raw_ticker["lastPrice"]),
        price_change_percent_24h=Decimal(raw_ticker["priceChangePercent"]),
        high_24h=Decimal(raw_ticker["highPrice"]),
        low_24h=Decimal(raw_ticker["lowPrice"]),
        volume_24h=Decimal(raw_ticker["volume"]),
    )


def get_top_coins(limit: int = 20) -> list[CoinTicker]:
    raw_tickers = binance_client.get_market_overview(limit=limit)
    return [_to_coin_ticker(t) for t in raw_tickers]


def get_coin(coin_symbol: str) -> CoinTicker:
    raw_ticker = binance_client.get_coin_ticker(coin_symbol)
    return _to_coin_ticker(raw_ticker)