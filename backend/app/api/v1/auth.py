from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user_data)


@router.post("/Login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    token = user_service.login_user(db, credentials)
    return Token(access_token=token)


@router.post("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user