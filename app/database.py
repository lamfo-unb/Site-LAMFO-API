from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os
import logging
from app.models import Base

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Test mode flag - when True, use SQLite instead of PostgreSQL
    TEST_MODE: bool = os.getenv("TEST_MODE", "false").lower() == "true"
    
    # SQLite settings for testing
    SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./test.db")
    
    # PostgreSQL connection settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "lamfo")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.getenv(
        "POSTGRES_HOST", "database"
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

# Database engine initialization
engine = None
SessionLocal = None


def create_database_engine():
    """Create and return a database engine, with fallback logic"""
    
    if settings.TEST_MODE:
        # SQLite for testing
        logger.info("Using SQLite database for testing")
        return create_engine(
            settings.database_url,
            connect_args={"check_same_thread": False}
        )
    
    # Try PostgreSQL for production
    logger.info("Attempting to connect to PostgreSQL...")
    logger.info(f"Host: {settings.POSTGRES_HOST}")
    logger.info(f"Port: {settings.POSTGRES_PORT}")
    logger.info(f"Database: {settings.POSTGRES_DB}")
    logger.info(f"User: {settings.POSTGRES_USER}")
    db_url_masked = (
        f"postgresql://{settings.POSTGRES_USER}:***@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
        f"{settings.POSTGRES_DB}"
    )
    logger.info(f"Database URL: {db_url_masked}")
    
    try:
        pg_engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,  # Check connection before using it
            pool_recycle=3600,   # Recycle connections after 1 hour
            pool_size=10,        # Connection pool size
            max_overflow=20,     # Max connections beyond pool_size
            connect_args={"connect_timeout": 30}  # 30 seconds timeout
        )
        # Only test connection in non-production or when explicitly requested
        env = os.getenv("ENVIRONMENT", "production").lower()
        test_connection = (
            os.getenv("TEST_DB_CONNECTION", "false").lower() == "true"
        )
        
        if env != "production" or test_connection:
            logger.info("Testing database connection...")
            with pg_engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.info(f"Connection test result: {result.fetchone()}")
            logger.info("✅ Successfully connected to PostgreSQL!")
        else:
            logger.info(
                "⚡ PostgreSQL engine created "
                "(connection will be tested on first use)"
            )
        
        return pg_engine
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        
        # In production, we require PostgreSQL
        env = os.getenv("ENVIRONMENT", "production").lower()
        if env == "production":
            logger.critical("PostgreSQL connection required for production.")
            raise
        
        # For development, fall back to SQLite
        logger.warning("Falling back to SQLite database for development")
        return create_engine(
            settings.SQLITE_URL,
            connect_args={"check_same_thread": False}
        )


def get_engine():
    """Get the database engine, creating it if necessary"""
    global engine
    if engine is None:
        engine = create_database_engine()
        # Create tables when engine is first created
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            logger.warning("Application may have limited functionality")
    return engine


def get_session_local():
    """Get the SessionLocal class, creating it if necessary"""
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine()
        )
    return SessionLocal


def get_db():
    """Get a database session"""
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
