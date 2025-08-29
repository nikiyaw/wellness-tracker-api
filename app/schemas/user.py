# Define data models for user creation and for the user object returned by the API

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Base Schema
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a new user
class UserCreate(UserBase):
    password: str

# Schema for returning user data (excluding password)
class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True