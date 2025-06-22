from fastapi import APIRouter, Depends
from app.wrappers.nbp_api import NBPClient as bank_api

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


@router.get("/")
async def create_item():

    exchange_rate = await bank_api().get_current_rate("eur")
    print(exchange_rate)

    exchange_rate = await bank_api().get_current_rate("rsd")
    print(exchange_rate)

    # table_data = await bank_api().get_exchange_table("B")
    # # print(table_data)
    # print(type(table_data))
    # for item in table_data[0]["rates"]:
    #     print(item)


    return "Hello world from wallets"


@router.get("/tester")
def create_item(token: str = Depends(oauth2_scheme)):
    print(token)
    return "Hello world from wallets"
