from sqlalchemy.orm import Session

from app.models.watchlist import Watchlist


def get_all_for_user(db: Session, user_id: int) -> list[Watchlist]:
    return db.query(Watchlist).filter(Watchlist.user_id == user_id).all()


def get_by_user_and_coin(db: Session, user_id: int, coin_symbol: str) -> Watchlist | None:
    return (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id, Watchlist.coin_symbol == coin_symbol)
        .first()
    )


def create(db: Session, user_id: int, coin_symbol: str) -> Watchlist:
    new_entry = Watchlist(user_id=user_id, coin_symbol=coin_symbol)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def delete(db: Session, entry: Watchlist) -> None:
    db.delete(entry)
    db.commit()

    