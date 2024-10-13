# app/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from app.crud import get_user  # Import get_user from crud
from app.dependencies import get_db
from app.models import User
from app.utils import verify_password  # Import verify_password from utils

router = APIRouter()

# Authenticate User
def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

# Fetch user ID from cookie and handle errors
def get_user_id_from_cookie(user_id: str = Cookie(None)):
    if not user_id or not user_id.isdigit():
        raise HTTPException(status_code=403, detail="Invalid or missing authentication cookie")
    return int(user_id)

# User login handler
@router.post("/login", response_model=None)  # Disable response model generation
async def login(response: Response, username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True, secure=True, samesite="Lax")
    return {"detail": "Login successful"}

# Get current user by session
async def get_current_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or missing authentication cookie")
    return user
