
import sys
import os
import pytest
import tempfile

# Set the TEST_MODE environment variable before importing any app modules
os.environ["TEST_MODE"] = "true"

# Add the project root directory to Python path so 'app' module can be found
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Now import from the app modules
from app.main import app
from app.database import get_db
from app.models import Base, Member, Project

@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine for each test"""
    # Create a temporary file for the test database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        test_db_path = tmp_file.name
    
    # Create engine with the temporary database
    engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False}
    )
    
    # Drop all tables if they exist and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    try:
        os.unlink(test_db_path)
    except Exception:
        pass

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Create a fresh database session for each test"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override"""
    def override_get_db():
        yield db_session
    
    # Clear any existing overrides first
    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear overrides after test
    app.dependency_overrides.clear()

@pytest.fixture
def sample_member_data():
    """Sample member data for testing"""
    import uuid
    return {
        "name": "Test User",
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
        "role": "Data Scientist",
        "bio": "Test bio",
        "github_username": f"testuser_{uuid.uuid4().hex[:8]}",
        "linkedin_url": "https://linkedin.com/in/testuser"
    }

@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        "title": "Test Project",
        "description": "Test project description",
        "status": "active",
        "github_url": "https://github.com/test/project",
        "demo_url": "https://demo.test.com"
    }