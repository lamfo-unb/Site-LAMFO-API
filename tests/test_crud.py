import pytest
from sqlalchemy.orm import Session
import app.crud as crud
import app.schemas as schemas
from app.models import Member, Project

class TestMemberCRUD:
    """Test member CRUD operations"""
    
    def test_create_member(self, db_session: Session):
        """Test creating a member"""
        member_data = schemas.MemberCreate(
            name="Test User",
            email="test@example.com",
            role="Data Scientist"
        )
        
        member = crud.create_member(db_session, member_data)
        
        assert member.name == "Test User"
        assert member.email == "test@example.com"
        assert member.role == "Data Scientist"
        assert member.id is not None
    
    def test_get_member_by_email(self, db_session: Session):
        """Test getting member by email"""
        # Create member
        member_data = schemas.MemberCreate(
            name="Test User",
            email="test@example.com"
        )
        created_member = crud.create_member(db_session, member_data)
        
        # Get by email
        found_member = crud.get_member_by_email(db_session, "test@example.com")
        
        assert found_member is not None
        assert found_member.id == created_member.id
        assert found_member.email == "test@example.com"
    
    def test_get_member_by_email_not_found(self, db_session: Session):
        """Test getting non-existent member by email"""
        member = crud.get_member_by_email(db_session, "nonexistent@example.com")
        assert member is None
    
    def test_get_members(self, db_session: Session):
        """Test getting all members"""
        # Create multiple members
        for i in range(3):
            member_data = schemas.MemberCreate(
                name=f"User {i}",
                email=f"user{i}@example.com"
            )
            crud.create_member(db_session, member_data)
        
        members = crud.get_members(db_session)
        assert len(members) == 3
    
    def test_update_member(self, db_session: Session):
        """Test updating a member"""
        # Create member
        member_data = schemas.MemberCreate(
            name="Original Name",
            email="test@example.com"
        )
        member = crud.create_member(db_session, member_data)
        
        # Update member
        update_data = schemas.MemberUpdate(name="Updated Name", role="Senior Data Scientist")
        updated_member = crud.update_member(db_session, member.id, update_data)
        
        assert updated_member is not None
        assert updated_member.name == "Updated Name"
        assert updated_member.role == "Senior Data Scientist"
        assert updated_member.email == "test@example.com"  # Should remain unchanged
    
    def test_delete_member(self, db_session: Session):
        """Test deleting a member"""
        # Create member
        member_data = schemas.MemberCreate(
            name="Test User",
            email="test@example.com"
        )
        member = crud.create_member(db_session, member_data)
        
        # Delete member
        success = crud.delete_member(db_session, member.id)
        assert success is True
        
        # Verify deletion
        deleted_member = crud.get_member(db_session, member.id)
        assert deleted_member is None

class TestProjectCRUD:
    """Test project CRUD operations"""
    
    def test_create_project(self, db_session: Session):
        """Test creating a project"""
        project_data = schemas.ProjectCreate(
            title="Test Project",
            description="Test description",
            status="active"
        )
        
        project = crud.create_project(db_session, project_data)
        
        assert project.title == "Test Project"
        assert project.description == "Test description"
        assert project.status == "active"
        assert project.id is not None
    
    def test_create_project_with_members(self, db_session: Session):
        """Test creating a project with assigned members"""
        # Create a member first
        member_data = schemas.MemberCreate(
            name="Test User",
            email="test@example.com"
        )
        member = crud.create_member(db_session, member_data)
        
        # Create project with member
        project_data = schemas.ProjectCreate(
            title="Test Project",
            member_ids=[member.id]
        )
        project = crud.create_project(db_session, project_data)
        
        assert len(project.members) == 1
        assert project.members[0].id == member.id
    
    def test_get_projects(self, db_session: Session):
        """Test getting all projects"""
        # Create multiple projects
        for i in range(3):
            project_data = schemas.ProjectCreate(
                title=f"Project {i}",
                description=f"Description {i}"
            )
            crud.create_project(db_session, project_data)
        
        projects = crud.get_projects(db_session)
        assert len(projects) == 3
    
    def test_update_project(self, db_session: Session):
        """Test updating a project"""
        # Create project
        project_data = schemas.ProjectCreate(
            title="Original Title",
            description="Original description"
        )
        project = crud.create_project(db_session, project_data)
        
        # Update project
        update_data = schemas.ProjectUpdate(
            title="Updated Title",
            status="completed"
        )
        updated_project = crud.update_project(db_session, project.id, update_data)
        
        assert updated_project is not None
        assert updated_project.title == "Updated Title"
        assert updated_project.status == "completed"
        assert updated_project.description == "Original description"  # Should remain unchanged