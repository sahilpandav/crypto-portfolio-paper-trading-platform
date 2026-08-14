from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.repositories import user_repository, wallet_repository
from app.schemas.user import UserCreate, UserLogin


def register_user(db: Session, user_data: UserCreate) -> User:
    existing_username = user_repository.get_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken.",
        )

    existing_email = user_repository.get_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    hashed = hash_password(user_data.password)

    new_user = user_repository.create(
        db,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
    )

    wallet_repository.create(
        db,
        user_id=new_user.id,
        balance=Decimal(str(settings.initial_virtual_balance)),
    )

    return new_user


def login_user(db: Session, credentials: UserLogin) -> str:
    user = user_repository.get_by_username(db, credentials.username)

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    return create_access_token(subject=str(user.id))