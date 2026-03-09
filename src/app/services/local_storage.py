import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.services.storage_backend import StorageBackend


class LocalStorage(StorageBackend):

    def save_file(self, upload: UploadFile, tenant_id: uuid.UUID) -> tuple[str, int]:
        # Create the tenant's upload directory if it doesn't exist
        tenant_dir = settings.UPLOAD_DIR / str(tenant_id)
        tenant_dir.mkdir(parents=True, exist_ok=True)

        # Generate a unique filename but keep the original extension

        original_name = upload.filename or "unnamed"
        extension = Path(original_name).suffix  # e.g. ".pdf"
        unique_name = f"{uuid.uuid4()}{extension}"

        file_path = tenant_dir / unique_name

        # Read the file contents and write to disk
        contents = upload.file.read()
        file_size = len(contents)

        # Check file size before saving
        if file_size > settings.MAX_FILE_SIZE:
            raise ValueError(f"File exceeds maximum size of {settings.MAX_FILE_SIZE} bytes")

        file_path.write_bytes(contents)

        # Return the relative path (what we store in the DB) and the size
        # We store relative paths so if we move the upload dir, nothing breaks
        return str(file_path.relative_to(settings.UPLOAD_DIR)), file_size

    def get_file_path(self, storage_path: str) -> Path:
        full_path = settings.UPLOAD_DIR / storage_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {storage_path}")

        return full_path

    def delete_file(self, storage_path: str) -> None:
        full_path = settings.UPLOAD_DIR / storage_path

        if full_path.exists():
            full_path.unlink()
