from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

router = APIRouter()


@router.get("/me", response_model = UserRead)
def get_me(user: User = Depends(get_current_user)):
    """Get current user profile"""
    return user


@router.put("/me", response_model = UserRead)
def update_me(updates: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user profile"""

    if updates.full_name is not None:
        user.full_name = updates.full_name
    
    if updates.email is not None:
        existing = db.query(User).filter(User.email == updates.email, User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")
    
        user.email = updates.email

    db.commit()
    db.refresh(user)

    return user
    



@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete current user account"""
    user.is_active = False
    db.commit()
