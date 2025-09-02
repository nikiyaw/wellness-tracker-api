from .user import User
from .habit import Habit

# We also need to define the reverse relationship on the User model. We must do this after both models are defined.
from sqlalchemy.orm import relationship
User.habits = relationship("Habit", back_populates="owner")