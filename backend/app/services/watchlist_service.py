from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import watchlist_repository
from app.services import market_service
from app.schemas.watchlist import WatchlistResponse
from app.models.watchlist import Watchlist


def add_to_watchlist(db: Session, user_id: int, coin_symbol: str) -> "Watchlist":
    coin_symbol = coin_symbol.upper()

    market_service.get_coin(coin_symbol)

    existing = watchlist_repository.get_by_user_and_coin(db, user_id, coin_symbol)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{coin_symbol} is already on your watchlist.",
        )

    return watchlist_repository.create(db, user_id, coin_symbol)


def get_my_watchlist(db: Session, user_id: int) -> list[WatchlistResponse]:
    entries = watchlist_repository.get_all_for_user(db, user_id)

    result = []
    for entry in entries:
        ticker = market_service.get_coin(entry.coin_symbol)
        result.append(
            WatchlistResponse(
                id=entry.id,
                coin_symbol=entry.coin_symbol,
                current_price=ticker.price,
                price_change_percent_24h=ticker.price_change_percent_24h,
                created_at=entry.created_at,
            )
        )

    return result


def remove_from_watchlist(db: Session, user_id: int, coin_symbol: str) -> None:
    coin_symbol = coin_symbol.upper()

    entry = watchlist_repository.get_by_user_and_coin(db, user_id, coin_symbol)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{coin_symbol} is not on your watchlist.",
        )

    watchlist_repository.delete(db, entry)