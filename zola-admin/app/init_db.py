from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app.models import User
from app.crud import create_user, get_user

def init_db():
    # Create tables based on models
    Base.metadata.create_all(bind=engine)

    # Create a new database session
    db = SessionLocal()

    try:
        # Check if the admin user exists
        admin_user = get_user(db, "admin")

        # If admin user doesn't exist, create one
        if not admin_user:
            create_user(db, username="admin", password="admin123")
            print("Default admin user created (username: admin, password: admin123)")

    # Ensure session is closed even if an error occurs
    finally:
        db.close()
