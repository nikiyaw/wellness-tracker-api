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


@router.get("/{habit_id}", response_model=HabitSchema)
def read_habit(habit_id: int, db: Session = Depends(get_db)):
    # Query the database for a specific habit by its ID.
    db_habit = db.query(HabitModel).filter(HabitModel.id == habit_id).first()

    # If the habit is not found, raise a 404 error. 
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Return the found SQLAlchemy model.
    return db_habit


@router.put("/{habit_id}", response_model=HabitSchema)
def update_habit(habit_id: int, habit: HabitUpdate, db: Session = Depends(get_db)):
    # First, find the habit we want to update. 
    db_habit = db.query(HabitModel).filter(HabitModel.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Update the SQLAlchemy model with the new data (allow partial updates for certain fields)
    for key, value in habit.model_dump(exclude_unset=True).items():
        setattr(db_habit, key, value)

    # Commit the changes. 
    db.commit()
    db.refresh(db_habit)
    return db_habit