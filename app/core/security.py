from passlib.context import CryptContext

# This CryptContext object tells Passlib what hashing algorithm to use and manages the hashing and verification process. 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashes a password using bcrypt.
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verifies a plain-text password against a stored hashed password.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)