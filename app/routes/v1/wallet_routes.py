from fastapi import APIRouter, HTTPException, Response
from fastapi import Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.wrappers.nbp_api import NBPClient as bank_api
from app.services.currency_service import CurrencyService as currency_service
from app.services.user_service import UserService as users_service
from app.services.wallet_service import WalletService
from app.schemas.user_schemas import UserResponse
from app.schemas.wallet_schemas import WalletCurrency
from app.db import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


@router.get("/")
async def get_data(db: Session = Depends(get_db), current_user: UserResponse = Depends(users_service.get_current_user)):
    wallet_service = WalletService(db)
    currency_amounts = await wallet_service.get_user_currencies_in_pln(current_user)
    return currency_amounts


@router.post("/sub/{currency_code}/{amount}", summary="Subtract currency from wallet")
@router.post("/add/{currency_code}/{amount}", summary="Add currency to wallet")
def add_currency_to_wallet(
    request: Request,
    data: WalletCurrency,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(users_service.get_current_user),
):

    data.currency_code = data.currency_code.upper()
    wallet_service = WalletService(db)

    valid_currencies_list = currency_service(db).get_currency_codes_as_list()
    if data.currency_code not in valid_currencies_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Currency '{data.currency_code}' is not supported."
        )

    wallet_id = wallet_service.get_default_wallet(current_user.id).id if data.wallet_id == 0 else data.wallet_id
    if wallet_service.check_if_wallet_belongs_to_user(current_user.id, wallet_id):
        if "add" in request.url.path:
            wallet_service.add_currency(wallet_id, data.currency_code, data.amount)
        else:
            wallet_service.subtract_currency(wallet_id, data.currency_code, data.amount)

        return JSONResponse(
            status_code=200,
            content={"message": "Operation Successful"}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Wallet does not belong to you."
        )
