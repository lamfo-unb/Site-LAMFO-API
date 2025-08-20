from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os
from app.models import Base

class Settings(BaseSettings):
    # Test mode flag - when True, use SQLite instead of PostgreSQL
    TEST_MODE: bool = os.getenv("TEST_MODE", "false").lower() == "true"
    
    # SQLite settings for testing
    SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./test.db")
    
    # PostgreSQL connection settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "lamfo")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.getenv(
        "POSTGRES_HOST", "database.1.uyp0svq7o4zphkxe880tjqkjd"
    )
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "lamfo_db")
    
    # Construct the database URL
    @property
    def database_url(self) -> str:
        if self.TEST_MODE:
            return self.SQLITE_URL
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    class Config:
        env_file = ".env"


settings = Settings()

# Create engine with appropriate settings based on database type
if settings.TEST_MODE:
    # SQLite for testing
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL for production
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,  # Check connection before using it
        pool_recycle=3600,   # Recycle connections after 1 hour
    )

# Create tables
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
