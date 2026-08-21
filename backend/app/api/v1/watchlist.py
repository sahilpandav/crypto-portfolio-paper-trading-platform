from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.watchlist import WatchlistCreate, WatchlistResponse
from app.services import watchlist_service

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@router.post("", status_code=201)
def add_to_watchlist(
    watchlist_data: WatchlistCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = watchlist_service.add_to_watchlist(db, current_user.id, watchlist_data.coin_symbol)
    return {"id": entry.id, "coin_symbol": entry.coin_symbol}


@router.get("", response_model=list[WatchlistResponse])
def get_my_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return watchlist_service.get_my_watchlist(db, current_user.id)


@router.delete("/{symbol}", status_code=204)
def remove_from_watchlist(
    symbol: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    watchlist_service.remove_from_watchlist(db, current_user.id, symbol)