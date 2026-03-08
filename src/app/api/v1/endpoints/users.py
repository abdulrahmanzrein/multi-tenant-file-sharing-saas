from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services import user_service

router = APIRouter()


@router.get("/me", response_model = UserRead)
def get_me(user: User = Depends(get_current_user)):
    """Get current user profile"""
    return user


@router.put("/me", response_model = UserRead)
def update_me(updates: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user profile"""
    return user_service.update_user(db, user, updates)
    


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete current user account"""
    user_service.delete_user(db, user)