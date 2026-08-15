from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.integrations.binance_client import get_current_price
from app.models.trade import Trade, TradeType
from app.repositories import wallet_repository, holding_repository, trade_repository
from app.schemas.trade import TradeRequest


def buy(db: Session, user_id: int, trade_data: TradeRequest) -> Trade:
    wallet = wallet_repository.get_by_user_id(db, user_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found for this user.",
        )

    current_price = get_current_price(trade_data.coin_symbol)
    total_cost = trade_data.quantity * current_price

    if total_cost > wallet.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient wallet balance for this trade.",
        )

    new_wallet_balance = wallet.balance - total_cost
    wallet_repository.update_balance(db, wallet, new_wallet_balance)

    existing_holding = holding_repository.get_by_user_and_coin(db, user_id, trade_data.coin_symbol)

    if existing_holding:
        total_quantity = existing_holding.quantity + trade_data.quantity
        existing_cost = existing_holding.quantity * existing_holding.average_buy_price
        new_cost = trade_data.quantity * current_price
        new_average_price = (existing_cost + new_cost) / total_quantity

        holding_repository.update(
            db,
            existing_holding,
            quantity=total_quantity,
            average_buy_price=new_average_price,
        )
    else:
        holding_repository.create(
            db,
            user_id=user_id,
            coin_symbol=trade_data.coin_symbol,
            quantity=trade_data.quantity,
            average_buy_price=current_price,
        )

    new_trade = trade_repository.create(
        db,
        user_id=user_id,
        coin_symbol=trade_data.coin_symbol,
        trade_type=TradeType.BUY,
        quantity=trade_data.quantity,
        price_at_trade=current_price,
        total_value=total_cost,
    )

    db.commit()
    db.refresh(new_trade)

    return new_trade


def sell(db: Session, user_id: int, trade_data: TradeRequest) -> Trade:
    wallet = wallet_repository.get_by_user_id(db, user_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found for this user.",
        )

    existing_holding = holding_repository.get_by_user_and_coin(db, user_id, trade_data.coin_symbol)

    if not existing_holding or existing_holding.quantity < trade_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient holdings for this trade.",
        )

    current_price = get_current_price(trade_data.coin_symbol)
    total_proceeds = trade_data.quantity * current_price

    new_wallet_balance = wallet.balance + total_proceeds
    wallet_repository.update_balance(db, wallet, new_wallet_balance)

    remaining_quantity = existing_holding.quantity - trade_data.quantity

    if remaining_quantity == 0:
        holding_repository.delete(db, existing_holding)
    else:
        holding_repository.update_quantity(db, existing_holding, remaining_quantity)

    new_trade = trade_repository.create(
        db,
        user_id=user_id,
        coin_symbol=trade_data.coin_symbol,
        trade_type=TradeType.SELL,
        quantity=trade_data.quantity,
        price_at_trade=current_price,
        total_value=total_proceeds,
    )

    db.commit()
    db.refresh(new_trade)

    return new_trade