from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import Member, Project
from app.schemas import MemberCreate, MemberUpdate, ProjectCreate, ProjectUpdate

# Member CRUD
def get_member(db: Session, member_id: int) -> Optional[Member]:
    return db.query(Member).filter(Member.id == member_id).first()

def get_member_by_email(db: Session, email: str) -> Optional[Member]:
    return db.query(Member).filter(Member.email == email).first()

def get_members(db: Session, skip: int = 0, limit: int = 100) -> List[Member]:
    return db.query(Member).offset(skip).limit(limit).all()

def create_member(db: Session, member: MemberCreate) -> Member:
    db_member = Member(
        name=member.name,
        email=member.email,
        role=member.role,
        bio=member.bio,
        github_username=member.github_username,
        # Convert HttpUrl to string if present
        linkedin_url=str(member.linkedin_url) if member.linkedin_url else None
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member_id: int, member: MemberUpdate) -> Optional[Member]:
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if db_member:
        update_data = member.model_dump(exclude_unset=True)
        # Convert HttpUrl to string if present in update
        if 'linkedin_url' in update_data and update_data['linkedin_url']:
            update_data['linkedin_url'] = str(update_data['linkedin_url'])
        
        for field, value in update_data.items():
            setattr(db_member, field, value)
        
        db.commit()
        db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int) -> bool:
    db_member = get_member(db, member_id)
    if db_member:
        db.delete(db_member)
        db.commit()
        return True
    return False

# Project CRUD
def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: ProjectCreate) -> Project:
    project_data = project.model_dump()
    member_ids = project_data.pop("member_ids", [])
    
    # Convert HttpUrl objects to strings
    if 'github_url' in project_data and project_data['github_url']:
        project_data['github_url'] = str(project_data['github_url'])
    if 'demo_url' in project_data and project_data['demo_url']:
        project_data['demo_url'] = str(project_data['demo_url'])
    
    db_project = Project(**project_data)
    
    # Add members to project
    if member_ids:
        members = db.query(Member).filter(Member.id.in_(member_ids)).all()
        db_project.members = members
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Optional[Project]:
    db_project = get_project(db, project_id)
    if db_project:
        update_data = project.model_dump(exclude_unset=True)
        member_ids = update_data.pop("member_ids", None)
        
        # Convert HttpUrl objects to strings if present in update
        if 'github_url' in update_data and update_data['github_url']:
            update_data['github_url'] = str(update_data['github_url'])
        if 'demo_url' in update_data and update_data['demo_url']:
            update_data['demo_url'] = str(update_data['demo_url'])
        
        # Update basic fields
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        # Update members if provided
        if member_ids is not None:
            members = db.query(Member).filter(Member.id.in_(member_ids)).all()
            db_project.members = members
        
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int) -> bool:
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False
