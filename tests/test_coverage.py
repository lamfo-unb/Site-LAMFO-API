import pytest
from app import populate_db
from app.models import MsgPayload, MemberRole, ProjectStatus
from app.schemas import MemberCreate, ProjectCreate

# Test populate_db.create_mock_data runs without error
def test_create_mock_data_runs(monkeypatch):
    class DummySession:
        def add(self, obj): pass
        def commit(self): pass
        def rollback(self): pass
        def close(self): pass
    monkeypatch.setattr(populate_db, "SessionLocal", lambda: DummySession())
    monkeypatch.setattr(populate_db, "engine", object())
    monkeypatch.setattr(populate_db.Base.metadata, "create_all", lambda bind: None)
    populate_db.create_mock_data()

# Test MsgPayload Pydantic model
def test_msgpayload_model():
    payload = MsgPayload(msg_id=1, msg_name="test")
    assert payload.msg_id == 1
    assert payload.msg_name == "test"

# Test MemberRole and ProjectStatus enums
def test_memberrole_enum():
    assert MemberRole.DATA_SCIENTIST.value == "Data Scientist"
    assert MemberRole.RESEARCHER.value == "Researcher"
    assert MemberRole.STUDENT.value == "Student"
    assert MemberRole.PROFESSOR.value == "Professor"

def test_projectstatus_enum():
    assert ProjectStatus.ACTIVE.value == "active"
    assert ProjectStatus.COMPLETED.value == "completed"
    assert ProjectStatus.ON_HOLD.value == "on_hold"
    assert ProjectStatus.CANCELLED.value == "cancelled"

# Test schema validation for MemberCreate and ProjectCreate
def test_membercreate_schema():
    data = {"name": "Test", "email": "test@example.com"}
    member = MemberCreate(**data)
    assert member.name == "Test"
    assert member.email == "test@example.com"

def test_projectcreate_schema():
    data = {"title": "Test Project"}
    project = ProjectCreate(**data)
    assert project.title == "Test Project"
    assert project.status == "active"
