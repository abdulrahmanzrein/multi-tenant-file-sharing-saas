from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.file import File
from app.models.user import User
from app.schemas.file import FileRead
from app.services import storage_service

router = APIRouter()


@router.post("/upload", response_model=FileRead, status_code=status.HTTP_201_CREATED)
def upload_file(
    upload: UploadFile,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Step 1: check storage limit (YOUR CODE — fixed indentation and storage_limit reference)
    if user.tenant.storage_used >= user.tenant.storage_limit:
        raise HTTPException(status_code=413, detail="Tenant storage is maxed out")

    # Step 2: save file to disk (YOUR CODE — fixed the unpacking)
    storage_path, file_size = storage_service.save_file(upload, user.tenant_id)

    # Step 3: create the DB record
    db_file = File(
        original_filename=upload.filename or "unnamed",
        storage_path=storage_path,
        content_type=upload.content_type or "application/octet-stream",
        size=file_size,
        owner_id=user.id,
        tenant_id=user.tenant_id,
    )
    db.add(db_file)

    # Step 4: update tenant storage
    user.tenant.storage_used += file_size

    # Step 5: commit and return
    db.commit()
    db.refresh(db_file)
    return db_file


@router.get("/", response_model=list[FileRead])
def list_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    files = db.query(File).filter(
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    ).all()
    return files


@router.get("/{file_id}", response_model=FileRead)
def get_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_file = db.query(File).filter(
        File.id == file_id,
        File.tenant_id == user.tenant_id,
        File.is_deleted == False,
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    return db_file


@router.get("/{file_id}/download")
def download_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

    return FileResponse(
        path=file_path,
        filename=db_file.original_filename,
        media_type=db_file.content_type,
    )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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
