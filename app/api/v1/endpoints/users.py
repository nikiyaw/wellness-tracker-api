# Create a API router to handle user-related requests (creating & reading a user)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.database.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, User as UserSchema

from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.core.security import verify_password
from app.core.auth import create_access_token

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)

    new_user = UserModel(email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user