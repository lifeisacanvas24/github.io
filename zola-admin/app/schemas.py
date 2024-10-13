# app/schemas.py
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True  # Use 'from_attributes' for Pydantic v2


class UserCreate(UserBase):
    password: str = Field(..., example="example_password")  # Password field for user creation

    class Config:
        from_attributes = True  # Use 'from_attributes' for Pydantic v2


class UserUpdate(BaseModel):
    username: str | None = None  # Optional username for updates
    password: str | None = None  # Optional password for updates

    class Config:
        from_attributes = True  # Use 'from_attributes' for Pydantic v2


class User(UserBase):
    id: int  # User ID is included in responses

    class Config:
        from_attributes = True  # Use 'from_attributes' for Pydantic v2
