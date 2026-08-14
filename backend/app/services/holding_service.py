from decimal import Decimal

from sqlalchemy.orm import Session

from app.integrations.binance_client import get_current_price
from app.repositories import holding_repository
from app.schemas.holding import HoldingResponse


def get_my_portfolio(db: Session, user_id: int) -> list[HoldingResponse]:
    holdings = holding_repository.get_all_for_user(db, user_id)

    portfolio = []
    for holding in holdings:
        current_price = get_current_price(holding.coin_symbol)
        current_value = holding.quantity * current_price
        cost_basis = holding.quantity * holding.average_buy_price
        profit_loss = current_value - cost_basis

        if cost_basis > 0:
            profit_loss_percent = (profit_loss / cost_basis) * Decimal("100")
        else:
            profit_loss_percent = Decimal("0")

        portfolio.append(
            HoldingResponse(
                id=holding.id,
                coin_symbol=holding.coin_symbol,
                quantity=holding.quantity,
                average_buy_price=holding.average_buy_price,
                current_price=current_price,
                current_value=current_value,
                profit_loss=profit_loss,
                profit_loss_percent=profit_loss_percent,
                updated_at=holding.updated_at,
            )
        )

    return portfolio