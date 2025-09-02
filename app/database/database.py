from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# The create_engine function is the starting point for any SQLAlchemy application.
# It creates a connection pool and manages the low-level communication with the database.
engine = create_engine(settings.DATABASE_URL)

# The sessionmaker creates a SessionLocal class. Each instance of SessionLocal is a database session.
# The session is your "staging area" for all the changes you want to make to the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base() returns a base class that our models will inherit from.
# This base class contains all the metadata for our database tables.
Base = declarative_base()

# This is a key FastAPI concept: a dependency for getting a database session.
# FastAPI's dependency injection system will call this function for each request that needs a database connection.
def get_db():
    db = SessionLocal()
    try:
        # The 'yield' keyword makes this a generator. The code before 'yield' runs first (opens the session).
        yield db
    finally: 
        # The code in the 'finally' block runs after the request is complete, ensuring the database session is always closed, even if an error occurs.
        db.close()