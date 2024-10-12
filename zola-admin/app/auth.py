from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from app.crud import get_user, verify_password
from app.dependencies import get_db
from app.models import User
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Improved: Authenticate User
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

# Improved: Fetch user ID from cookie and handle errors
def get_user_id_from_cookie(user_id: str = Cookie(None)):
    if not user_id or not user_id.isdigit():
        raise HTTPException(status_code=403, detail="Invalid or missing authentication cookie")
    return int(user_id)

# User login handler
@router.post("/login")
async def login(response: Response, username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True, secure=True, samesite="Lax")
    return {"detail": "Login successful"}

# Get current user by session
async def get_current_user(db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie()  # Your cookie retrieval logic
    logging.info(f"Attempting to retrieve user ID: {user_id}")
    if user_id is None:
        logging.warning("User ID is None. User is not authenticated.")
        return None
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logging.warning("No user found for the provided ID.")
        return None
    logging.info(f"Authenticated user: {user.username}")
    return user
