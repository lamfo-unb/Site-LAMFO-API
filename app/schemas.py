from pydantic import BaseModel, EmailStr, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import datetime

from app.models import MemberRole, ProjectStatus

# Member schemas
class MemberBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = None
    bio: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    bio: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None

class Member(MemberBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    projects: List["ProjectSummary"] = []

# Project schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "active"
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None

class ProjectCreate(ProjectBase):
    member_ids: Optional[List[int]] = []

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    member_ids: Optional[List[int]] = None

class ProjectSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    status: str

class Project(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    members: List["MemberSummary"] = []

class MemberSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    email: str
    role: Optional[str] = None

# Update forward references
Member.model_rebuild()
Project.model_rebuild()