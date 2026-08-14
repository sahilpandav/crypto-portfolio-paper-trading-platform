from decimal import Decimal 

from sqlalchemy.orm import Session

from app.models.wallet import Wallet


def get_by_user_id(db: Session, user_id: int) -> Wallet | None:
    return db.query(Wallet).filter(Wallet.user_id == user_id).first()


def create(db: Session, user_id: int, balance: Decimal) -> Wallet:
    new_wallet = Wallet(user_id=user_id, balance=balance)
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    return new_wallet