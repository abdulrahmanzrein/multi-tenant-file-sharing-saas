from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.services import share_service, storage_service

router = APIRouter()


@router.post("/files/{file_id}/share")
def create_share_link(
    file_id: UUID,
    expires_at: Optional[datetime] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    link = share_service.create_share_link(db, user, file_id, expires_at)
    return {"token": link.token}


@router.get("/share/{token}")
def download_shared_file(
    token: str,
    db: Session = Depends(get_db),
):
    link, db_file = share_service.resolve_token(db, token)
    file_path = storage_service.storage.get_file_path(db_file.storage_path)
    return FileResponse(
        path=file_path,
        filename=db_file.original_filename,
        media_type=db_file.content_type,
    )