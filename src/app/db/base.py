from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class that all database models inherit from.

    Example:
        class User(Base):
            __tablename__ = "users"
            id = Column(Integer, primary_key=True)
    """
    pass


class TimestampMixin:
    """
    Add this to any model to automatically track when rows
    are created and updated.

    Example:
        class User(TimestampMixin, Base):
            __tablename__ = "users"
            ...
        # Now every User row will have created_at and updated_at columns
    """

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )
