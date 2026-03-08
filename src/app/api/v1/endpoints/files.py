from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.file import FileRead
from app.services import file_service

router = APIRouter()


@router.post("/upload", response_model=FileRead, status_code=status.HTTP_201_CREATED)
def upload_file(
    upload: UploadFile,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return file_service.upload_file(db, user, upload)



@router.get("/", response_model=list[FileRead])
def list_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return file_service.list_files(db, user)


@router.get("/{file_id}", response_model=FileRead)
def get_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return file_service.get_file(db, user, file_id)


@router.get("/{file_id}/download")
def download_file(
    file_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_path, db_file = file_service.get_download_path(db, user, file_id)
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
    file_service.delete_file(db, user, file_id)