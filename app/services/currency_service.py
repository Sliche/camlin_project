from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.currency_model import Currency as CurrencyModel
from app.services.base_service import BaseService
from app.wrappers.nbp_api import NBPClient as bank_api


class CurrencyService(BaseService):

    def __init__(self, db: Session):
        self.model = CurrencyModel
        super().__init__(db)

    def get_currency_codes_as_list(self):
        currency_codes = self.db.scalars(select(self.model.code)).all()
        return currency_codes

    async def add_new_currencies(self):
        existing_codes = set(code for (code,) in self.db.query(self.model.code).all())
        table_data_a = await bank_api().get_exchange_table("A")
        table_data_b = await bank_api().get_exchange_table("B")
        a_rates = table_data_a[0]["rates"]
        b_rates = table_data_b[0]["rates"]
        all_currencies = a_rates + b_rates

        for item in all_currencies:
            if item["code"] not in existing_codes:
                currency = self.model()
                currency.code = item["code"]
                currency.state = item["currency"]
                self.db.add(currency)
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
