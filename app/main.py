from fastapi import FastAPI

from app.routes.v1 import wallet_routes
from app.routes.v1 import user_routes

app = FastAPI()

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(wallet_routes.router, prefix="/wallet", tags=["Wallets"])

