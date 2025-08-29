# To handle password hasing and verification logic

from passlib.context import CryptContext

pwd_context = CryptContext(schemas=["bcrypt"], deprecated="auto")

# Hash a password using bcrypt
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify a plain password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)