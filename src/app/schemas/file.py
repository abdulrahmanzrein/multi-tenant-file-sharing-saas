from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

# What should the API RETURN about a file?
class FileRead(BaseModel):
    id: UUID
    original_filename: str
    size: int
    content_type: str
    created_at: datetime
    owner_id: UUID

    model_config = ConfigDict(from_attributes=True)

class PaginatedFiles(BaseModel):
    total: int
    items: list[FileRead]

    