from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate



def update_user(db: Session, user: User, updates: UserUpdate) -> User:
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

def delete_user(db: Session, user: User) -> None:
    user.is_active = False
    db.commit()
