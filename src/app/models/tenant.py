import uuid

from sqlalchemy import Column, String, Boolean, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Tenant(TimestampMixin, Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)  # url-friendly name like "acme-corp"
    is_active = Column(Boolean, default=True)

    # each tenant gets a storage limit in bytes (default 5GB)
    storage_limit = Column(BigInteger, default=5368709120)
    storage_used = Column(BigInteger, default=0)

    # a tenant has many users and many files
    users = relationship("User", back_populates="tenant")
    files = relationship("File", back_populates="tenant")
