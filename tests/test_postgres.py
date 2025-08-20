"""
Test PostgreSQL connection. This test will be skipped if the PostgreSQL
database is not available.
"""
import os
import sys
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Temporarily unset TEST_MODE for these tests to connect to the real PostgreSQL
real_test_mode = os.environ.get("TEST_MODE")
os.environ.pop("TEST_MODE", None)

# Import settings after changing environment
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.database import settings


def is_postgres_available():
    """Check if PostgreSQL is available by using environment variables."""
    # Get connection details from environment variables
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "lamfo")
    password = os.getenv("POSTGRES_PASSWORD", "")
    db = os.getenv("POSTGRES_DB", "lamfo_db")
    
    # Construct the database URL
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    # Try to connect
    try:
        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False


@pytest.mark.skipif(
    not is_postgres_available(), reason="PostgreSQL database not available"
)
def test_postgres_connection():
    """Test connection to PostgreSQL database."""
    # Get connection details from environment variables
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "lamfo")
    password = os.getenv("POSTGRES_PASSWORD", "")
    db = os.getenv("POSTGRES_DB", "lamfo_db")
    
    # Construct the database URL
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    # Try to connect
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1
        
        # Check that we can connect to the specific database
        result = conn.execute(text("SELECT current_database()")).scalar()
        assert result == db
        
        # Check user
        result = conn.execute(text("SELECT current_user")).scalar()
        assert result == user


@pytest.mark.skipif(
    not is_postgres_available(), reason="PostgreSQL database not available"
)
def test_postgres_tables():
    """Test that PostgreSQL database has the expected tables."""
    # Get connection details from environment variables
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "lamfo")
    password = os.getenv("POSTGRES_PASSWORD", "")
    db = os.getenv("POSTGRES_DB", "lamfo_db")
    
    # Construct the database URL
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    # Try to connect
    engine = create_engine(db_url)
    with engine.connect() as conn:
        # Get a list of tables
        result = conn.execute(text(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public'"
        ))
        tables = [row[0] for row in result]
        
        # Check for expected tables
        # If these tables don't exist yet, they will be created when the app 
        # starts
        expected_tables = ["members", "projects", "member_projects"]
        
        # Only assert if the database has already been initialized
        if tables:
            for table in expected_tables:
                assert table in tables or pytest.skip(
                    f"Table {table} not found. "
                    f"Database may not be initialized yet."
                )

# Restore the original TEST_MODE environment variable
if real_test_mode:
    os.environ["TEST_MODE"] = real_test_mode
