from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
def register():
    """Register a new user"""
    return {"message": "Register endpoint - TODO"}


@router.post("/login")
def login():
    """Login and get JWT token"""
    return {"message": "Login endpoint - TODO"}


@router.post("/refresh")
def refresh_token():
    """Refresh JWT token"""
    return {"message": "Refresh token endpoint - TODO"}
