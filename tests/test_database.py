"""
Test database connection and CRUD operations.
"""
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.database import settings
from app.models import Base, Member, Project
from app import crud, schemas

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_db():
    """Create a test database session."""
    # Ensure we're in test mode
    import os
    os.environ["TEST_MODE"] = "true"
    
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for a test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)


def test_database_connection():
    """Test that we can connect to the test database."""
    engine = create_engine(TEST_DATABASE_URL)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            assert result == 1
    except OperationalError as e:
        pytest.fail(f"Failed to connect to database: {e}")


def test_create_member(test_db):
    """Test creating a member in the database."""
    member_data = schemas.MemberCreate(
        name="Test User",
        email="test@example.com",
        role="Data Scientist",
        bio="A test user",
        github_username="testuser",
        linkedin_url="https://linkedin.com/in/testuser"
    )
    
    # Create the member
    member = crud.create_member(test_db, member=member_data)
    
    # Verify the member was created with the right data
    assert member.name == "Test User"
    assert member.email == "test@example.com"
    assert member.role == "Data Scientist"
    
    # Check that we can retrieve the member
    db_member = crud.get_member(test_db, member_id=member.id)
    assert db_member is not None
    assert db_member.name == member.name
    assert db_member.email == member.email


def test_create_project(test_db):
    """Test creating a project in the database."""
    project_data = schemas.ProjectCreate(
        title="Test Project",
        description="A test project",
        status="active",
        github_url="https://github.com/test/project",
        demo_url="https://demo.example.com"
    )
    
    # Create the project
    project = crud.create_project(test_db, project=project_data)
    
    # Verify the project was created with the right data
    assert project.title == "Test Project"
    assert project.description == "A test project"
    assert project.status == "active"
    
    # Check that we can retrieve the project
    db_project = crud.get_project(test_db, project_id=project.id)
    assert db_project is not None
    assert db_project.title == project.title
    assert db_project.description == project.description


def test_get_members(test_db):
    """Test retrieving a list of members."""
    # Create multiple members
    members_data = [
        schemas.MemberCreate(name="User 1", email="user1@example.com", role="Researcher"),
        schemas.MemberCreate(name="User 2", email="user2@example.com", role="Professor"),
        schemas.MemberCreate(name="User 3", email="user3@example.com", role="Student")
    ]
    
    for member_data in members_data:
        crud.create_member(test_db, member=member_data)
    
    # Retrieve all members
    members = crud.get_members(test_db)
    assert len(members) == 3
    
    # Check for expected data
    emails = [member.email for member in members]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails
    assert "user3@example.com" in emails


def test_get_projects(test_db):
    """Test retrieving a list of projects."""
    # Create multiple projects
    projects_data = [
        schemas.ProjectCreate(title="Project 1", description="Description 1", status="active"),
        schemas.ProjectCreate(title="Project 2", description="Description 2", status="completed"),
        schemas.ProjectCreate(title="Project 3", description="Description 3", status="on_hold")
    ]
    
    for project_data in projects_data:
        crud.create_project(test_db, project=project_data)
    
    # Retrieve all projects
    projects = crud.get_projects(test_db)
    assert len(projects) == 3
    
    # Check for expected data
    titles = [project.title for project in projects]
    assert "Project 1" in titles
    assert "Project 2" in titles
    assert "Project 3" in titles
