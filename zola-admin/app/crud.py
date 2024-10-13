# app/crud.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request  # Import Request from FastAPI
from app.models import User
from app.schemas import UserCreate  # Ensure this is the updated version without email
from app.utils import hash_password
import logging

# Function to retrieve a user by username
def get_user(db: Session, username: str):
    """Retrieve a user by username."""
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Function to get the user from the session token
async def get_user_from_token(request: Request):
    """Retrieve user from the session token."""
    token = request.cookies.get("session_token")
    # Logic to fetch the user from the token or session
    # This should return a User object
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await get_user_by_token(token)  # Implement this function to return a User object
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# Function to create a new user
def create_user(db: Session, user: UserCreate):
    """Create a new user in the database."""
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password must be provided.")

    existing_user = get_user(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")

    db_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return db_user
