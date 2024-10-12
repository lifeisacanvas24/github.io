#app/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from app.crud import get_user, verify_password
from app.dependencies import get_db
from app.models import User
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db, username=username)
    if user and verify_password(password, user.hashed_password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

def get_user_id_from_cookie(user_id: str = Cookie(None)):
    if user_id is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return int(user_id)

@router.post("/login")
async def login(response: Response, username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    response.set_cookie(key="user_id", value=str(user.id), httponly=True)
    return {"detail": "Login successful"}

def get_current_user(db: Session = Depends(get_db), user_id: int = Depends(get_user_id_from_cookie)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    return user
