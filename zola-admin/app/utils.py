# app/utils.py
from passlib.context import CryptContext

# Create a password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Helper function to hash passwords
def hash_password(password: str) -> str:
    """Hash a password using pbkdf2_sha256."""
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a provided password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
