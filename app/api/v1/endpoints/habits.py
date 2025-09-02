from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.habit import Habit as HabitModel
from app.models.user import User as UserModel
from app.schemas.habit import HabitCreate, HabitUpdate, Habit as HabitSchema
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=HabitSchema, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit: HabitCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):

    # Now, instead of a hardcoded user_id, we use the ID from the authenticated user.
    db_habit = HabitModel(**habit.model_dump(), user_id=current_user.id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


@router.get("/", response_model=List[HabitSchema])
def read_habits(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)):

    # We filter the query to only return habits that belong to the current user.
    habits = db.query(HabitModel).filter(HabitModel.user_id == current_user.id).all()
    return habits


@router.get("/{habit_id}", response_model=HabitSchema)
def read_habit(
    habit_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)):

    # The query now filters by both the habit's ID and the user's ID.
    db_habit = db.query(HabitModel).filter(
        HabitModel.id == habit_id,
        HabitModel.user_id == current_user.id
    ).first()

    # Raising a 404 is a good practice to avoid leaking information.
    # We don't say "Habit found but you're not the owner."
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit


@router.put("/{habit_id}", response_model=HabitSchema)
def update_habit(
    habit_id: int, 
    habit: HabitUpdate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):

    db_habit = db.query(HabitModel).filter(
        HabitModel.id == habit_id,
        HabitModel.user_id == current_user.id
    ).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    for key, value in habit.model_dump(exclude_unset=True).items():
        setattr(db_habit, key, value)

    db.commit()
    db.refresh(db_habit)
    return db_habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_habit = db.query(HabitModel).filter(
        HabitModel.id == habit_id,
        HabitModel.user_id == current_user.id
    ).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(db_habit)
    db.commit()
    return