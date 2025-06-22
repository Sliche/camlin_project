from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.base import TimestampMixin
from app.db import Base
from app.models.constants import STATUS_ACTIVE


class User(Base, TimestampMixin):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(120), unique=True, nullable=False)

    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    username = Column(String(128), nullable=True, unique=True)
    password = Column(String(128), nullable=False)

    status = Column(String(32), nullable=True, default=STATUS_ACTIVE)

    wallets = relationship("Wallet", back_populates="owner", cascade="all, delete-orphan")
