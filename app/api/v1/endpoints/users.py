from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, User as UserSchema

router = APIRouter()

@router.post("/", repsonse_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email already exists to prevent duplicate users.
    # .filter() builds a query, and .first() retireves the first result or None.
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    # If the user exists, raise an HTTP exception.
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Securely hash the user's password before storing it.
    hashed_password = user.password

    # Create a new user object using the SQLAlchemy model. 
    new_user = UserModel(email=user.email, password_hash=hashed_password)

    # Add the new user to the database session.
    db.add(new_user)

    # Commit the transaction to save the new user to the database. 
    db.commit()

    # Refresh the object to get the user's ID and other default values from the database. 
    db.refresh(new_user)

    # Return the new user object, which FastAPI will convert to the UserSchema.
    return new_user



