from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.habit import Habit as HabitModel
from app.schemas.habit import HabitCreate, HabitUpdate, Habit as HabitSchema

router = APIRouter()

@router.post("/", response_model=HabitSchema, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    # For now, we will hardcode a user_id. We will add real authentication later. 
    user_id = 1

    # 1. Create a SQLAlchemy model instance from the validated Pydantic data.
    db_habit = HabitModel(**habit.model_dump(), user_id=user_id)

    # 2. Add the new object to the database session. 
    db.add(db_habit)

    # 3. Commit the changes to the database. 
    db.commit()

    # 4. Refresh the object to get the ID and other database-generated data.
    db.refresh(db_habit)

    # 5. Return the SQLAlchemy model, which FastAPI will automatically convert to the Pydantic HabitSchema.
    return db_habit

@router.get("/", response_model=List[HabitSchema])
def read_habits(db: Session = Depends(get_db)):
    # For now, hardcode user_id.
    user_id = 1

    # Query the database to get all habits for the hardcoded user.
    habits = db.query(HabitModel).filter(HabitModel.user_id == user_id).all()

    # Return the list of SQLAlchemy models. FastAPI will convert them to Pydantic schemas.
    return habits