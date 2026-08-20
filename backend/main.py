from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.wallet import router as wallet_router
from app.api.v1.portfolio import router as portfolio_router
from app.api.v1.trade import router as trade_router
from app.api.v1.market import router as market_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(wallet_router, prefix="/api/v1")
app.include_router(portfolio_router, prefix="/api/v1")
app.include_router(trade_router, prefix="/api/v1")
app.include_router(market_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    db_status = "unreachable"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "unreachable"

    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "database": db_status,
    }