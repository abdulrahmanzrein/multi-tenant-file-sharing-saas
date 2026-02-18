import uuid
from pathlib import Path
 
from fastapi import UploadFile

from app.core.config import settings


def save_file(upload: UploadFile, tenant_id: uuid.UUID) -> tuple[str, int]:
    """
    Save an uploaded file to disk.

    We store files at: uploads/files/<tenant_id>/<unique_filename>
    - tenant_id keeps each tenant's files separate
    - unique filename (uuid) prevents collisions if two users upload "report.pdf"

    Returns (storage_path, file_size) so the caller can save these to the database.
    """

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


def get_file_path(storage_path: str) -> Path:
    """
    Convert a stored relative path back to an absolute path on disk.
    This is what we use when someone wants to download a file.
    """
    full_path = settings.UPLOAD_DIR / storage_path

    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {storage_path}")

    return full_path


def delete_file(storage_path: str) -> None:
    """
    Delete a file from disk.
    We don't raise an error if it's already gone — that's fine.
    """
    full_path = settings.UPLOAD_DIR / storage_path

    if full_path.exists():
        full_path.unlink()
