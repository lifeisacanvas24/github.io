
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
from passlib.context import CryptContext
from fastapi import HTTPException

# Use Argon2 hashing scheme
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Helper function to hash passwords
def hash_password(password: str) -> str:
    """Hash a password using pbkdf2_sha256."""
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a provided password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# Function to retrieve a user by username
def get_user(db: Session, username: str):
    """Retrieve a user by username."""
    return db.query(User).filter(User.username == username).first()

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
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return db_user

# Function to retrieve all users
def get_users(db: Session):
    """Retrieve a list of all users."""
    return db.query(User).all()

# Function to retrieve a user by user ID
def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user by their unique ID."""
    return db.query(User).filter(User.id == user_id).first()

# Function to update a user's information
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Update a user's information."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update username and optionally the password
    db_user.username = user_update.username
    if user_update.password:  # Hash the password only if it's provided
        db_user.hashed_password = hash_password(user_update.password)

    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return db_user

# Function to delete a user by ID
def delete_user(db: Session, user_id: int):
    """Delete a user by their ID."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
