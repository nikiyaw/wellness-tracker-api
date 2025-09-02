from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitBase(BaseModel):
    name: str
    category: Optional[str] = None
    frequency: Optional[str] = None

class HabitCreate(HabitBase):
    pass # This schema is identical to the base for now, but we separate it for clarity.

class HabitUpdate(HabitBase):
    streak: Optional[int] = None
    last_logged: Optional[datetime] = None

class Habit(HabitBase):
    id: int
    user_id: int
    streak: Optional[int] = None
    last_logged: Optional[datetime] = None

    class Config:
        from_attributes = True