from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db():
    """
    Creates a database session for each request.

    How it works:
    - Opens a new database session
    - 'yield' gives it to the endpoint to use
    - After the endpoint is done, 'finally' closes the session

    Usage in endpoints:
        @router.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
