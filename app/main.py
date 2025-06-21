from fastapi import FastAPI

from app.routes.v1 import wallet
from app.routes.v1 import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallets"])

