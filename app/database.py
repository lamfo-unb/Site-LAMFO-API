from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Use SQLite for local testing, PostgreSQL for production
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./lamfo_test.db")
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create engine with appropriate settings for SQLite vs PostgreSQL
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url, 
        connect_args={"check_same_thread": False}  # SQLite specific
    )
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()