#app/schemas.py
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True  # Enable Pydantic to create models from attributes


class UserCreate(BaseModel):
    username: str = Field(..., example="example_username")
    password: str = Field(..., example="example_password")


class UserUpdate(BaseModel):
    username: str
    password: str | None = None  # Optional password for updates

    class Config:
        from_attributes = True  # Ensure from_attributes is used in place of orm_mode


class User(UserBase):
    id: int  # User ID is included in responses

    class Config:
        from_attributes = True  # Ensure from_attributes is used in place of orm_mode
