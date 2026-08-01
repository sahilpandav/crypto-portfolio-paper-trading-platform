from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

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