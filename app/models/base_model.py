from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, TIMESTAMP, func


Base = declarative_base()


class TimestampMixin:
    __abstract__ = True

    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
