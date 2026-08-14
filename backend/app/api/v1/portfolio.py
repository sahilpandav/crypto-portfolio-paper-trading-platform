from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.holding import HoldingResponse
from app.services import holding_service

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/me", response_model=list[HoldingResponse])
def get_my_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return holding_service.get_my_portfolio(db, current_user.id)