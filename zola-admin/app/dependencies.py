from fastapi import Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal  # Ensure SessionLocal is imported
from app.models import User  # Import User model

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the current user based on a cookie
def get_user_id_from_cookie(user_id: str = Cookie(None)):
    """Retrieve the user ID from the cookie."""
    if user_id is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return int(user_id)  # Ensure the user_id is converted to int

def get_current_user(db: Session = Depends(get_db), user_id: int = Depends(get_user_id_from_cookie)):
    """Retrieve the current user based on the user ID from the cookie."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
