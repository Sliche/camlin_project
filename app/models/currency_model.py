from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.base_model import TimestampMixin
from app.db import Base
from app.models.wallet_currency_model import WalletCurrency


class Currency(Base, TimestampMixin):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    state = Column(String(128), nullable=True)
    code = Column(String(10), unique=True, nullable=False)

    wallet_amounts = relationship("WalletCurrency", back_populates="currency")

