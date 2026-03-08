from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.user import User
from app.services import storage_service


def upload_file(db: Session, user: User, upload: UploadFile) -> File:
    if user.tenant.storage_used >= user.tenant.storage_limit:
        raise HTTPException(status_code=413, detail="Tenant storage is maxed out")

    
    storage_path, file_size = storage_service.save_file(upload, user.tenant_id)


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
    return db_file


def list_files(db: Session, user: User) -> list[File]:
    files = db.query(File).filter(
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    ).all()

    return files


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
        file_path = storage_service.get_file_path(db_file.storage_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found on disk")

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

    storage_service.delete_file(db_file.storage_path)

    db_file.is_deleted = True
    user.tenant.storage_used -= db_file.size

    db.commit()
