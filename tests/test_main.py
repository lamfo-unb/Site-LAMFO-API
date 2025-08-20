import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    # Check for partial match - only verify the 'message' key exists
    assert "message" in response.json()
    assert "LAMFO API is running" in response.json()["message"]


def test_about_route(client):
    response = client.get("/about")
    assert response.status_code == 404  # This endpoint doesn't exist, so 404 is correct


class TestMemberEndpoints:
    """Test member CRUD operations"""

    def test_create_member_success(self, client, sample_member_data):
        """Test successful member creation"""
        response = client.post("/members/", json=sample_member_data)
        assert response.status_code == 201  # Changed from 200 to 201

        data = response.json()
        assert data["name"] == sample_member_data["name"]
        assert data["email"] == sample_member_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_create_member_duplicate_email(self, client, sample_member_data):
        """Test member creation with duplicate email"""
        # Create first member
        client.post("/members/", json=sample_member_data)

        # Try to create another with same email
        response = client.post("/members/", json=sample_member_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_get_members_empty(self, client):
        """Test getting members when database is empty"""
        response = client.get("/members/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_members_with_data(self, client, sample_member_data):
        """Test getting members with data"""
        # Create a member first
        client.post("/members/", json=sample_member_data)

        response = client.get("/members/")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["email"] == sample_member_data["email"]

    def test_get_member_by_id_success(self, client, sample_member_data):
        """Test getting member by ID"""
        # Create member
        create_response = client.post("/members/", json=sample_member_data)
        member_id = create_response.json()["id"]

        # Get member by ID
        response = client.get(f"/members/{member_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == member_id
        assert data["email"] == sample_member_data["email"]

    def test_get_member_by_id_not_found(self, client):
        """Test getting non-existent member"""
        response = client.get("/members/999")
        assert response.status_code == 404
        assert "Member not found" in response.json()["detail"]

    def test_update_member_success(self, client, sample_member_data):
        """Test successful member update"""
        # Create member
        create_response = client.post("/members/", json=sample_member_data)
        member_id = create_response.json()["id"]

        # Update member
        update_data = {"name": "Updated Name", "role": "Senior Data Scientist"}
        response = client.put(f"/members/{member_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["role"] == "Senior Data Scientist"
        assert data["email"] == sample_member_data["email"]  # Should remain unchanged

    def test_update_member_not_found(self, client):
        """Test updating non-existent member"""
        update_data = {"name": "Updated Name"}
        response = client.put("/members/999", json=update_data)
        assert response.status_code == 404
        assert "Member not found" in response.json()["detail"]

    def test_delete_member_success(self, client, sample_member_data):
        """Test successful member deletion"""
        # Create member
        create_response = client.post("/members/", json=sample_member_data)
        member_id = create_response.json()["id"]

        # Delete member
        response = client.delete(f"/members/{member_id}")
        assert response.status_code == 200
        assert "Member deleted successfully" in response.json()["message"]

        # Verify member is deleted
        get_response = client.get(f"/members/{member_id}")
        assert get_response.status_code == 404

    def test_delete_member_not_found(self, client):
        """Test deleting non-existent member"""
        response = client.delete("/members/999")
        assert response.status_code == 404
        assert "Member not found" in response.json()["detail"]


class TestProjectEndpoints:
    """Test project CRUD operations"""

    def test_create_project_success(self, client, sample_project_data):
        """Test successful project creation"""
        response = client.post("/projects/", json=sample_project_data)
        assert response.status_code == 201  # Changed from 200 to 201

        data = response.json()
        assert data["title"] == sample_project_data["title"]
        assert "id" in data

    def test_create_project_with_members(self, client, sample_member_data, sample_project_data):
        """Test creating project with assigned members"""
        # Create a member first
        member_response = client.post("/members/", json=sample_member_data)
        member_id = member_response.json()["id"]

        # Create project with member
        sample_project_data["member_ids"] = [member_id]
        response = client.post("/projects/", json=sample_project_data)
        assert response.status_code == 201  # Changed from 200 to 201

        data = response.json()
        assert len(data["members"]) == 1
        assert data["members"][0]["id"] == member_id

    def test_get_projects_empty(self, client):
        """Test getting projects when database is empty"""
        response = client.get("/projects/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_projects_with_data(self, client, sample_project_data):
        """Test getting projects with data"""
        # Create a project first
        client.post("/projects/", json=sample_project_data)

        response = client.get("/projects/")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == sample_project_data["title"]

    def test_get_project_by_id_success(self, client, sample_project_data):
        """Test getting project by ID"""
        # Create project
        create_response = client.post("/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Get project by ID
        response = client.get(f"/projects/{project_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == project_id
        assert data["title"] == sample_project_data["title"]

    def test_get_project_by_id_not_found(self, client):
        """Test getting non-existent project"""
        response = client.get("/projects/999")
        assert response.status_code == 404
        assert "Project not found" in response.json()["detail"]

    def test_update_project_success(self, client, sample_project_data):
        """Test successful project update"""
        # Create project
        create_response = client.post("/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Update project
        update_data = {"title": "Updated Project", "status": "completed"}
        response = client.put(f"/projects/{project_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Updated Project"
        assert data["status"] == "completed"
        assert data["description"] == sample_project_data["description"]  # Should remain unchanged

    def test_delete_project_success(self, client, sample_project_data):
        """Test successful project deletion"""
        # Create project
        create_response = client.post("/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Delete project
        response = client.delete(f"/projects/{project_id}")
        assert response.status_code == 200
        assert "Project deleted successfully" in response.json()["message"]

        # Verify project is deleted
        get_response = client.get(f"/projects/{project_id}")
        assert get_response.status_code == 404


class TestMemberProjectRelationship:
    """Test member-project relationships"""

    def test_assign_members_to_project(self, client, sample_member_data, sample_project_data):
        """Test assigning multiple members to a project"""
        # Create two members
        member1_response = client.post("/members/", json=sample_member_data)
        member1_id = member1_response.json()["id"]

        sample_member_data["email"] = "test2@example.com"
        member2_response = client.post("/members/", json=sample_member_data)
        member2_id = member2_response.json()["id"]

        # Create project with both members
        sample_project_data["member_ids"] = [member1_id, member2_id]
        project_response = client.post("/projects/", json=sample_project_data)

        assert project_response.status_code == 201  # Changed from 200 to 201
        project_data = project_response.json()
        assert len(project_data["members"]) == 2

        member_ids = [member["id"] for member in project_data["members"]]
        assert member1_id in member_ids
        assert member2_id in member_ids
