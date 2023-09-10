# Import necessary modules from SQLAlchemy and project-specific modules.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Form the database URL from the settings provided
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

# Create the database engine using the URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a declarative base for the models
Base = declarative_base()

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    # Create a new session
    db = SessionLocal()
    try:
        # Yield the session to be used by the caller
        yield db
    finally:
        # Close the session when done
        db.close()