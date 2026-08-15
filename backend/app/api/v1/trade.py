from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.trade import TradeRequest, TradeResponse
from app.services import trade_service

router = APIRouter(prefix="/trade", tags=["Trading"])


@router.post("/buy", response_model=TradeResponse, status_code=201)
def buy(
    trade_data: TradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return trade_service.buy(db, current_user.id, trade_data)