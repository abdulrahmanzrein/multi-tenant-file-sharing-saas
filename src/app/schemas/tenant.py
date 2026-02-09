from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Schema for creating a tenant
class TenantCreate(BaseModel):
    name: str
    slug: str


# Schema for reading a tenant
class TenantRead(BaseModel):
    name: str
    slug: str
    id: UUID
    is_active: bool
    storage_limit: int 
    storage_used: int
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True  # tells Pydantic to read from SQLAlchemy models