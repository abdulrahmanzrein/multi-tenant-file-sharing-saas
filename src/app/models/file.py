import uuid

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class File(TimestampMixin, Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # what the user originally named the file
    original_filename = Column(String(255), nullable=False)

    # where we actually stored it (could be s3 key or local path)
    storage_path = Column(String(500), nullable=False)

    # mime type like "application/pdf" or "image/png"
    content_type = Column(String(100), nullable=False)

    # file size in bytes
    size = Column(Integer, nullable=False)

    # soft delete - we don't actually remove files right away
    is_deleted = Column(Boolean, default=False)

    # who uploaded this file
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="files")

    # which tenant this file belongs to (for scoping queries)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    tenant = relationship("Tenant", back_populates="files")
