from sqlalchemy.orm import Session

from app.models.holding import Holding


def get_all_for_user(db: Session, user_id: int) -> list[Holding]:
    return db.query(Holding).filter(Holding.user_id == user_id).all()


def get_by_user_and_coin(db: Session, user_id: int, coin_symbol: str) -> Holding | None:
    return (
        db.query(Holding)
        .filter(Holding.user_id == user_id, Holding.coin_symbol == coin_symbol)
        .first()
    )