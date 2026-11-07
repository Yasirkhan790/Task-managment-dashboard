"""Registration and login endpoints."""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.dependencies import DatabaseSession, CurrentUser
from app.models import User
from app.schemas import TokenResponse, UserCreate, UserResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: DatabaseSession) -> User:
    existing_user = db.scalar(select(User).where(User.email == user_data.email))
    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=user_data.email, full_name=user_data.full_name, hashed_password=hash_password(user_data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login_user(db: DatabaseSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == form_data.username))
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(access_token=create_access_token(str(user.id)))

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: CurrentUser) -> User:
    return current_user
