from sqlalchemy.orm import Session

from app.models.trade import Trade, TradeType


def create(
    db: Session,
    user_id: int,
    coin_symbol: str,
    trade_type: TradeType,
    quantity,
    price_at_trade,
    total_value,
) -> Trade:
    new_trade = Trade(
        user_id=user_id,
        coin_symbol=coin_symbol,
        trade_type=trade_type,
        quantity=quantity,
        price_at_trade=price_at_trade,
        total_value=total_value,
    )
    db.add(new_trade)
    return new_trade


def get_all_for_user(db: Session, user_id: int) -> list[Trade]:
    return (
        db.query(Trade)
        .filter(Trade.user_id == user_id)
        .order_by(Trade.created_at.desc())
        .all()
    )