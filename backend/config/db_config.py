from fastapi import Depends
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from ..models.base import Base  
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration settings
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/weights/best_model.pt") 

    def validate(self):
        if not self.DATABASE_URL:
            logging.error("DATABASE_URL not found in environment variables.")
            raise ValueError("DATABASE_URL must be set in the environment variables.")

# Create settings instance and validate
settings = Settings()
settings.validate()

# Create database engine
try:
    engine = create_engine(settings.DATABASE_URL)
    logging.info("Database engine created successfully.")
except Exception as e:
    logging.error(f"Error creating database engine: {e}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    """Provide a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Database session error: {e}")
        raise
    finally:
        db.close()

# Debugging: Check database connection
def check_database():
    """Check if the database is accessible and print existing tables."""
    try:
        with engine.connect() as connection:
            inspector = inspect(connection)
            tables = inspector.get_table_names()
            logging.info(f"Connected to database: {engine.url.database}")
            logging.info(f"Existing tables: {tables if tables else 'No tables found'}")
    except Exception as e:
        logging.error(f"Error checking database connection: {e}")
