from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.wallet import WalletResponse
from app.services import wallet_service

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.get("/me", response_model=WalletResponse)
def get_my_wallet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return wallet_service.get_my_wallet(db, current_user.id)