from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class WalletCurrency(Base):
    __tablename__ = "wallet_currencies"

    id = Column(Integer, primary_key=True)

    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False, default=0.0)

    wallet = relationship("Wallet", back_populates="currency_amounts")
    currency = relationship("Currency", back_populates="wallet_amounts")

    __table_args__ = (UniqueConstraint("wallet_id", "currency_id", name="uix_wallet_currency"),)
