from fastapi import APIRouter

router = APIRouter()


@router.post("/upload")
def upload_file():
    """Upload a file"""
    return {"message": "Upload file - TODO"}


@router.get("/{file_id}")
def get_file(file_id: int):
    """Get file metadata"""
    return {"message": f"Get file {file_id} - TODO"}


@router.get("/{file_id}/download")
def download_file(file_id: int):
    """Download a file"""
    return {"message": f"Download file {file_id} - TODO"}


@router.delete("/{file_id}")
def delete_file(file_id: int):
    """Delete a file"""
    return {"message": f"Delete file {file_id} - TODO"}


@router.get("/")
def list_files():
    """List user's files"""
    return {"message": "List files - TODO"}
