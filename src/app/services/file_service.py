from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.user import User
from app.services import storage_service
from app.services import audit_service


def upload_file(db: Session, user: User, upload: UploadFile) -> File:
    if user.tenant.storage_used >= user.tenant.storage_limit:
        raise HTTPException(status_code=413, detail="Tenant storage is maxed out")

    
    storage_path, file_size = storage_service.storage.save_file(upload, user.tenant_id)


    db_file = File(
        original_filename=upload.filename or "unnamed",
        storage_path=storage_path,
        content_type=upload.content_type or "application/octet-stream",
        size=file_size,
        owner_id=user.id,
        tenant_id=user.tenant_id,
    )
    db.add(db_file)

    
    user.tenant.storage_used += file_size

    
    db.commit()
    db.refresh(db_file)
    audit_service.log_action(db, user.id, user.tenant_id, "file.upload", db_file.id)
    return db_file


def list_files(db: Session, user: User, skip: int = 0, limit: int = 20) -> tuple[list[File], int]:
    query = db.query(File).filter(
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    )
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_file(db: Session, user: User, file_id: UUID) -> File:
    db_file = db.query(File).filter(
        File.id == file_id,
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    return db_file


def get_download_path(db: Session, user: User, file_id: UUID) -> tuple[str, File]:
    db_file = db.query(File).filter(
        File.id == file_id,
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        file_path = storage_service.storage.get_file_path(db_file.storage_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found on disk")

    audit_service.log_action(db, user.id, user.tenant_id, "file.download", db_file.id)
    return file_path, db_file


def delete_file(db: Session, user: User, file_id: UUID) -> None:
    db_file = db.query(File).filter(
        File.id == file_id,
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    if db_file.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this file")

    storage_service.storage.delete_file(db_file.storage_path)

    db_file.is_deleted = True
    user.tenant.storage_used -= db_file.size

    db.commit()
    audit_service.log_action(db, user.id, user.tenant_id, "file.delete", db_file.id)
