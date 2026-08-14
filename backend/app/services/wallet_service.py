from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.wallet import Wallet
from app.repositories import wallet_repository


def get_my_wallet(db: Session, user_id: int) -> Wallet:
    wallet = wallet_repository.get_by_user_id(db, user_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found for this user.",
        )
    return wallet