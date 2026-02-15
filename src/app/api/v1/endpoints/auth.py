from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)

    new_user = User(email=user.email, hashed_password=hashed, full_name=user.full_name, role=user.role, tenant_id=user.tenant_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login():
    """Login and get JWT token"""
    return {"message": "Login endpoint - TODO"}


@router.post("/refresh")
def refresh_token():
    """Refresh JWT token"""
    return {"message": "Refresh token endpoint - TODO"}
