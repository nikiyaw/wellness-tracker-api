from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    category = Column(String)
    frequency = Column(String)
    streak = Column(Integer, default=0)
    last_logged = Column(DateTime)

    owner = relationship("User", back_populates="habits")