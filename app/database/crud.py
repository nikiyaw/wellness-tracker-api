from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.schemas import user as UserSchema

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def create_user(db: Session, email: str, password_hash: str):
    db_user = UserModel(email=email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user