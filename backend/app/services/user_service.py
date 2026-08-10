from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import UserCreate


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

    return new_user