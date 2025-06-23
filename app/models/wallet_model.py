from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base_model import TimestampMixin
from app.db import Base
from app.models.wallet_currency_model import WalletCurrency


class Wallet(Base, TimestampMixin):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    default = Column(Boolean, default=False, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="wallets")
    currency_amounts = relationship("WalletCurrency", back_populates="wallet", cascade="all, delete-orphan")
