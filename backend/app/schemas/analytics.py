from decimal import Decimal

from pydantic import BaseModel


class CoinAllocation(BaseModel):
    coin_symbol: str
    current_value: Decimal
    allocation_percent: Decimal


class PortfolioSummary(BaseModel):
    total_invested: Decimal
    total_current_value: Decimal
    total_profit_loss: Decimal
    total_profit_loss_percent: Decimal
    wallet_balance: Decimal
    net_worth: Decimal
    allocations: list[CoinAllocation]