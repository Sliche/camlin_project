from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.currency_model import Currency as CurrencyModel
from app.services.base_service import BaseService


class CurrencyService(BaseService):

    def __init__(self, db: Session):
        self.model = CurrencyModel
        super().__init__(db)

    def get_currency_codes_as_list(self):
        currency_codes = self.db.scalars(select(self.model.code)).all()
        return currency_codes
