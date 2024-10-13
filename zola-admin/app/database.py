# app/database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Define the path for the database file
db_path = os.path.join(os.path.dirname(__file__), 'zola_admin.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"  # Correct format for SQLite

# Create engine and session local
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Create all database tables if they don't exist.
    Call this function during the startup of your FastAPI application.
    """
    Base.metadata.create_all(bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

# Add additional models as needed
class AnotherModel(Base):
    __tablename__ = "another_table"

    id = Column(Integer, primary_key=True, index=True)
    some_field = Column(String)

# You can define more models here as required
