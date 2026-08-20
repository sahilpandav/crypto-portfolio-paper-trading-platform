from fastapi import APIRouter

from app.schemas.market import CoinTicker
from app.services import market_service

router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/coins", response_model=list[CoinTicker])
def get_top_coins(limit: int = 20):
    return market_service.get_top_coins(limit=limit)


@router.get("/coins/{symbol}", response_model=CoinTicker)
def get_coin(symbol: str):
    return market_service.get_coin(symbol)