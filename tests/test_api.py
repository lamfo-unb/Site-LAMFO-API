"""
Test the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas, crud


def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "LAMFO API is running",
        "status": "operational"
    }


def test_create_member(client):
    """Test creating a member via the API."""
    member_data = {
        "name": "Test User",
        "email": "test@example.com",
        "role": "Data Scientist",
        "bio": "A test user",
        "github_username": "testuser",
        "linkedin_url": "https://linkedin.com/in/testuser"
    }
    
    response = client.post("/members/", json=member_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == member_data["name"]
    assert data["email"] == member_data["email"]
    assert data["role"] == member_data["role"]
    assert "id" in data


def test_read_members(client):
    """Test reading members via the API."""
    # First create some members
    member_data_list = [
        {
            "name": "User 1",
            "email": "user1@example.com",
            "role": "Researcher"
        },
        {
            "name": "User 2",
            "email": "user2@example.com",
            "role": "Professor"
        }
    ]
    
    for member_data in member_data_list:
        client.post("/members/", json=member_data)
    
    # Now get the list of members
    response = client.get("/members/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    
    # Check that both members are in the response
    emails = [member["email"] for member in data]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails


def test_read_member(client):
    """Test reading a single member via the API."""
    # First create a member
    member_data = {
        "name": "Test User",
        "email": "test@example.com",
        "role": "Data Scientist"
    }
    
    create_response = client.post("/members/", json=member_data)
    created_member = create_response.json()
    member_id = created_member["id"]
    
    # Now get the member by ID
    response = client.get(f"/members/{member_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == member_id
    assert data["name"] == member_data["name"]
    assert data["email"] == member_data["email"]


def test_read_member_not_found(client):
    """Test reading a non-existent member."""
    response = client.get("/members/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Member not found"}


def test_create_project(client):
    """Test creating a project via the API."""
    project_data = {
        "title": "Test Project",
        "description": "A test project",
        "status": "active",
        "github_url": "https://github.com/test/project",
        "demo_url": "https://demo.example.com"
    }
    
    response = client.post("/projects/", json=project_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == project_data["title"]
    assert data["description"] == project_data["description"]
    assert data["status"] == project_data["status"]
    assert "id" in data


def test_read_projects(client):
    """Test reading projects via the API."""
    # First create some projects
    project_data_list = [
        {
            "title": "Project 1",
            "description": "Description 1",
            "status": "active"
        },
        {
            "title": "Project 2",
            "description": "Description 2",
            "status": "completed"
        }
    ]
    
    for project_data in project_data_list:
        client.post("/projects/", json=project_data)
    
    # Now get the list of projects
    response = client.get("/projects/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    
    # Check that both projects are in the response
    titles = [project["title"] for project in data]
    assert "Project 1" in titles
    assert "Project 2" in titles


def test_read_project(client):
    """Test reading a single project via the API."""
    # First create a project
    project_data = {
        "title": "Test Project",
        "description": "A test project",
        "status": "active"
    }
    
    create_response = client.post("/projects/", json=project_data)
    created_project = create_response.json()
    project_id = created_project["id"]
    
    # Now get the project by ID
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == project_id
    assert data["title"] == project_data["title"]
    assert data["description"] == project_data["description"]


def test_read_project_not_found(client):
    """Test reading a non-existent project."""
    response = client.get("/projects/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}
