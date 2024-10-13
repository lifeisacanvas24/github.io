# app/models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, constr
from app.utils import hash_password

Base = declarative_base()  # Ensure this is created once

# SQLAlchemy User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

# Pydantic models for user creation and response
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: constr(min_length=6)  # Minimum length for passwords

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # Enable compatibility with ORM objects

# Function to hash the password and create a new User object
def create_user_hashed(user: UserCreate):
    """Hash the password for a new user."""
    return User(username=user.username, hashed_password=hash_password(user.password))
