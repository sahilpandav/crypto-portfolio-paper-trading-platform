from decimal import Decimal

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


def create(db: Session, user_id: int, coin_symbol: str, quantity: Decimal, average_buy_price: Decimal) -> Holding:
    new_holding = Holding(
        user_id=user_id,
        coin_symbol=coin_symbol,
        quantity=quantity,
        average_buy_price=average_buy_price,
    )
    db.add(new_holding)
    return new_holding


def update(db: Session, holding: Holding, quantity: Decimal, average_buy_price: Decimal) -> Holding:
    holding.quantity = quantity
    holding.average_buy_price = average_buy_price
    db.add(holding)
    return holding