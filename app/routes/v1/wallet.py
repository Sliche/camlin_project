from fastapi import APIRouter, Depends
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


@router.post("/")
def create_item():
    return "Hello world from wallets"


@router.get("/tester")
def create_item(token: str = Depends(oauth2_scheme)):
    print(token)
    return "Hello world from wallets"
