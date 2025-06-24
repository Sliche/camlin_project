from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from fastapi import Depends, status

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.wrappers.jwt import JWTManager
from app.schemas.token_schemas import Token
from app.schemas.user_schemas import UserCreate, UserResponse, UserSchema, UpdateUserSchema
from app.services.user_service import UserService as users_service
from app.services.wallet_service import WalletService as wallet_service
from app.db import get_db


jwt_service = JWTManager()
router = APIRouter()


@router.get("/", response_model=UserResponse)
def get_user(current_user: UserResponse = Depends(users_service.get_current_user)):
    return current_user


@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    new_user = users_service(db).create(user_in)
    wallet_service(db).create_default_wallet(new_user.id)
    return new_user


@router.put("/", response_model=UserResponse)
def update_user(new_data: UpdateUserSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(users_service.get_current_user)):
    new_user = users_service(db).update(current_user.id, new_data)
    return new_user


@router.delete("/")
def delete_user(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(users_service.get_current_user)):
    users_service(db).delete(current_user.id)

    return JSONResponse(
        status_code=200,
        content={"message": "User deleted"}
    )


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = users_service.authenticate_user(db, form_data.username, form_data.password)

    if user:
        access_token = jwt_service.create_token({
            "sub": str(user.id)
        })

        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Something went wrong."
        )
