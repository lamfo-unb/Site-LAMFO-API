from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum

Base = declarative_base()

# Association table for many-to-many relationship between members and projects
member_project_association = Table(
    'member_projects',
    Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)

class MsgPayload(BaseModel):
    msg_id: Optional[int]
    msg_name: str

class MemberRole(str, Enum):
    DATA_SCIENTIST = "Data Scientist"
    RESEARCHER = "Researcher"
    STUDENT = "Student"
    PROFESSOR = "Professor"

class ProjectStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    github_username = Column(String(100), nullable=True)
    linkedin_url = Column(String(255), nullable=True)  # Changed from HttpUrl to String
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    projects = relationship("Project", secondary=member_project_association, back_populates="members")
    
    def __str__(self):
        return f"{self.name} ({self.role or 'No role'})"
    
    def __repr__(self):
        return (f"<Member(id={self.id}, name='{self.name}', "
                f"email='{self.email}')>")


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active")  # active, completed, paused
    github_url = Column(String(255), nullable=True)
    demo_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    members = relationship(
        "Member",
        secondary=member_project_association,
        back_populates="projects"
    )
    
    def __str__(self):
        return f"{self.title} ({self.status})"
    
    def __repr__(self):
        return (f"<Project(id={self.id}, title='{self.title}', "
                f"status='{self.status}')>")
