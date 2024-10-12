# app/cli-migrate.py

import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.database import SQLALCHEMY_DATABASE_URL, SessionLocal
from app.models import User
from passlib.context import CryptContext

# Initialize password context for hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def migrate_password():
    # Connect to the database
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with Session(engine) as session:
        # Query the user
        user = session.query(User).filter(User.username == "admin").first()  # Adjust username if needed
        if user:
            # Update the password with the new hash
            new_hashed_password = get_hashed_password("123admin")  # Replace with the desired new password
            user.hashed_password = new_hashed_password
            session.commit()
            print(f"Updated password for user {user.username}.")
        else:
            print("User not found.")

if __name__ == "__main__":
    migrate_password()

"""
5. Migrate Existing Passwords (Optional)

If you have multiple users and want to migrate their passwords without resetting them manually, you can implement a migration script that:

	1.	Attempts to verify the existing password.
	2.	If successful, rehashes it with pbkdf2_sha256 and updates the database.

Here’s a simple example of such a migration script:

def migrate_passwords():
    db = SessionLocal()
    users = db.query(User).all()
    for user in users:
        # Assuming the old hashing method is known and functional
        if user.hashed_password.startswith("$2b$"):  # Example for bcrypt
            try:
                # Attempt to verify the password with the old method
                plain_password = "get_password_somehow"  # Define how to get this
                if verify_password(plain_password, user.hashed_password):  # Using old verify function
                    user.hashed_password = hash_password(plain_password)
                    db.commit()
                    print(f"Updated password for user {user.username}.")
            except Exception as e:
                print(f"Error migrating password for {user.username}: {str(e)}")

    db.close()
""""
