from decimal import Decimal

import pandas as pd

from sqlalchemy.orm import Session

from app.integrations.binance_client import get_current_price
from app.repositories import holding_repository, wallet_repository
from app.schemas.analytics import CoinAllocation, PortfolioSummary


def get_portfolio_summary(db: Session, user_id: int) -> PortfolioSummary:
    wallet = wallet_repository.get_by_user_id(db, user_id)
    holdings = holding_repository.get_all_for_user(db, user_id)

    if not holdings:
        wallet_balance = wallet.balance if wallet else Decimal("0")
        return PortfolioSummary(
            total_invested=Decimal("0"),
            total_current_value=Decimal("0"),
            total_profit_loss=Decimal("0"),
            total_profit_loss_percent=Decimal("0"),
            wallet_balance=wallet_balance,
            net_worth=wallet_balance,
            allocations=[],
        )

    rows = []
    for holding in holdings:
        current_price = get_current_price(holding.coin_symbol)
        rows.append({
            "coin_symbol": holding.coin_symbol,
            "quantity": float(holding.quantity),
            "average_buy_price": float(holding.average_buy_price),
            "current_price": float(current_price),
        })

    df = pd.DataFrame(rows)

    df["invested"] = df["quantity"] * df["average_buy_price"]
    df["current_value"] = df["quantity"] * df["current_price"]

    total_invested = Decimal(str(df["invested"].sum()))
    total_current_value = Decimal(str(df["current_value"].sum()))
    total_profit_loss = total_current_value - total_invested

    if total_invested > 0:
        total_profit_loss_percent = (total_profit_loss / total_invested) * Decimal("100")
    else:
        total_profit_loss_percent = Decimal("0")

    df["allocation_percent"] = (df["current_value"] / df["current_value"].sum()) * 100

    allocations = [
        CoinAllocation(
            coin_symbol=row["coin_symbol"],
            current_value=Decimal(str(row["current_value"])),
            allocation_percent=Decimal(str(row["allocation_percent"])),
        )
        for _, row in df.iterrows()
    ]

    wallet_balance = wallet.balance if wallet else Decimal("0")
    net_worth = wallet_balance + total_current_value

    return PortfolioSummary(
        total_invested=total_invested,
        total_current_value=total_current_value,
        total_profit_loss=total_profit_loss,
        total_profit_loss_percent=total_profit_loss_percent,
        wallet_balance=wallet_balance,
        net_worth=net_worth,
        allocations=allocations,
    )