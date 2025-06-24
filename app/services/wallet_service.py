import os
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.models.wallet_model import Wallet as WalletModel
from app.models.wallet_currency_model import WalletCurrency
from app.models.currency_model import Currency
from app.services.base_service import BaseService
from app.wrappers.nbp_api import NBPClient as bank_api

from dotenv import load_dotenv
load_dotenv()


class WalletService(BaseService):

    def __init__(self, db: Session):
        self.model = WalletModel
        super().__init__(db)

    @staticmethod
    async def get_user_currencies_in_pln(user):
        wallets_data = []

        for wallet in user.wallets:
            total_pln_value = 0
            data = {
                "wallet_id": wallet.id,
                "wallet_name": wallet.name,
                "currencies": []
            }

            for currency_amount in wallet.currency_amounts:
                exchange_rate = await bank_api().get_current_rate(currency_amount.currency.code)
                pln_value = currency_amount.amount * exchange_rate
                data["currencies"].append({
                    "currency_code": currency_amount.currency.code,
                    "original_value": currency_amount.amount,
                    "pln_value": pln_value
                })
                total_pln_value += pln_value
            data["total_pln_value"] = total_pln_value

            wallets_data.append(data)
        return wallets_data

    def create_default_wallet(self, user_id):
        new_wallet = self.model()
        new_wallet.user_id = user_id
        new_wallet.name = os.getenv("DEFAULT_WALLET_NAME", "default_wallet")
        new_wallet.default = True
        try:
            self.db.add(new_wallet)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Something went wrong."
            )
        return new_wallet

    def get_default_wallet(self, user_id):
        default_wallet = self.db.query(self.model).filter(self.model.user_id == user_id,
                                                          self.model.default==True).first()

        return default_wallet

    def check_if_wallet_belongs_to_user(self, user_id, wallet_id):
        wallet = self.get_by_id(wallet_id)
        return True if (wallet and wallet.owner.id == user_id) else False

    def add_currency(self, wallet_id, currency_code, amount):

        currency = self.db.query(Currency).filter(Currency.code == currency_code).first()
        wallet_currency = self.db.query(WalletCurrency).filter(WalletCurrency.wallet_id == wallet_id,
                                                               WalletCurrency.currency_id == currency.id).first()
        if wallet_currency:
            wallet_currency.amount += amount
        else:
            wallet_currency = WalletCurrency()
            wallet_currency.currency_id = currency.id
            wallet_currency.wallet_id = wallet_id
            wallet_currency.amount = amount

        self.db.add(wallet_currency)
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()

    def subtract_currency(self, wallet_id, currency_code, amount):
        currency = self.db.query(Currency).filter(Currency.code == currency_code).first()
        wallet_currency = self.db.query(WalletCurrency).filter(WalletCurrency.wallet_id == wallet_id,
                                                               WalletCurrency.currency_id == currency.id).first()
        if not wallet_currency or wallet_currency.amount < amount:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User does not have enough credit."
            )
        else:
            wallet_currency.amount -= amount
            self.db.add(wallet_currency)
            self.db.commit()
