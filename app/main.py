from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.currency_service import CurrencyService as currency_service
from app.services.user_service import UserService as user_service
from app.services.wallet_service import WalletService as wallet_service
from app.routes.v1 import wallet_routes
from app.routes.v1 import user_routes

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    db: Session = next(get_db())
    try:
        await currency_service(db).add_new_currencies()
        user_service(db).create_initial_user()
    finally:
        db.close()


app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(wallet_routes.router, prefix="/wallet", tags=["Wallets"])

