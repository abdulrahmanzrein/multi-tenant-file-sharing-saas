from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
import secrets
from app.models.file import File
from app.models.shared_link import SharedLink
from app.models.user import User


def create_share_link(db: Session, user: User, file_id: UUID, expires_at: Optional[datetime] = None) -> SharedLink:
    db_file = db.query(File).filter(
        File.id == file_id,
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    token = secrets.token_hex(32)

    link = SharedLink(
        token=token,
        file_id=file_id,
        created_by=user.id,
        expires_at=expires_at,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

def resolve_token(db: Session, token: str) -> tuple[SharedLink, File]:
    link = db.query(SharedLink).filter(SharedLink.token == token).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    if link.expires_at and link.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="Link has expired")

    db_file = db.query(File).filter(
        File.id == link.file_id,
        File.is_deleted == False,
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    return link, db_file
