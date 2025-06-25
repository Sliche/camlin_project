from app.schemas.base_schema import BaseSchema
from pydantic import Field
from typing import Optional


class WalletCurrency(BaseSchema):
    currency_code: str

    amount: float = Field(
        default=1,
        ge=0,
        le=1_000_000,
    )

    # wallet_id: Optional[int] = Field(
    #     default=0,
    #     ge=0,
    #     description="Leave 0 to add to default wallet, or replace with exact wallet id you wish to add the funds to",
    # )
