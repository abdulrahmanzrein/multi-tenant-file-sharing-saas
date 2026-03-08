from pydantic import BaseModel, ConfigDict
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


    model_config = ConfigDict(from_attributes=True)