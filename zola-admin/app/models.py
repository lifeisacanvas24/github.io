from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import Table

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # Allow redefining the table if needed

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
