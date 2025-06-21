from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.wrappers.jwt import JWTManager
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse, UserSchema
from app.services.user_service import UserService
from app.db import get_db


jwt_service = JWTManager()
users_service = UserService()
router = APIRouter()


@router.get("/", response_model=UserResponse)
async def my_user(current_user: UserResponse = Depends(users_service.get_current_user)):
    return current_user


@router.post("/")
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    new_user = users_service.create_user(db, user_in)
    return new_user


@router.put("/")
async def edit_user(new_data: UserSchema, db: Session = Depends(get_db),
                    current_user: UserSchema = Depends(users_service.get_current_user)):
    new_user = users_service.edit_user(db, current_user.id, new_data)
    return new_user


@router.delete("/")
async def delete_user(db: Session = Depends(get_db),
                      current_user: UserSchema = Depends(users_service.get_current_user)):
    new_user = users_service.delete_user(db, current_user.id)
    return new_user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = users_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = jwt_service.create_token({
        "sub": str(user.id)
    })

    return Token(access_token=access_token, token_type="bearer")


