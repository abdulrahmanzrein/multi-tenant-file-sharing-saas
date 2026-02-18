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
    """
    Upload a file.

    TODO:
    1. Check if tenant has storage space left (user.tenant.storage_used vs storage_limit)
    2. Call storage_service.save_file(upload, user.tenant_id) — returns (storage_path, file_size)
    3. Create a File(...) DB record with the metadata
    4. Update tenant.storage_used += file_size
    5. db.commit() and db.refresh(), then return the file record
    """
    pass


@router.get("/", response_model=list[FileRead])
def list_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all non-deleted files for the current user's tenant.

    TODO:
    1. Query File where tenant_id == user.tenant_id and is_deleted == False
    2. Return the results
    """
    pass


@router.get("/{file_id}", response_model=FileRead)
def get_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get file metadata by ID.

    TODO:
    1. Query File by file_id, scoped to user's tenant, not deleted
    2. If not found, raise 404
    3. Return the file record
    """
    pass


@router.get("/{file_id}/download")
def download_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Download the actual file.

    TODO:
    1. Look up the File record (same query as get_file)
    2. Call storage_service.get_file_path(db_file.storage_path) to get the disk path
    3. Return FileResponse(path=..., filename=db_file.original_filename, media_type=db_file.content_type)
    """
    pass


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Soft-delete a file.

    TODO:
    1. Look up the File record (scoped to tenant, not already deleted)
    2. Check db_file.owner_id == user.id (only owner can delete)
    3. Call storage_service.delete_file(db_file.storage_path) to remove from disk
    4. Set db_file.is_deleted = True
    5. Subtract the file size from tenant.storage_used
    6. db.commit()
    """
    pass
