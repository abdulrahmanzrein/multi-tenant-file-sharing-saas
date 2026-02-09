from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

# What does a client send to register?
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str
    tenant_id: UUID


# What does the API return about a user?
class UserRead(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    tenant_id: UUID
    is_active: bool
    id: UUID

    class Config:
        from_attributes = True
