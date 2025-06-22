from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.base import TimestampMixin
from app.db import Base
from app.models.constants import STATUS_ACTIVE


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="wallets")
