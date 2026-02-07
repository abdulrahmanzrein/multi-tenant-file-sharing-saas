from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
def get_current_user():
    """Get current user profile"""
    return {"message": "Get current user - TODO"}


@router.put("/me")
def update_current_user():
    """Update current user profile"""
    return {"message": "Update user - TODO"}


@router.delete("/me")
def delete_current_user():
    """Delete current user account"""
    return {"message": "Delete user - TODO"}
