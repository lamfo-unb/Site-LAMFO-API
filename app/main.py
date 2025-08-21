from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import logging
import os
from . import models, schemas, crud
from .database import get_db
from .admin import create_admin

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI app
app = FastAPI(
    title="LAMFO API",
    description="API for managing LAMFO members and projects",
    root_path="/api"  # This tells FastAPI it's mounted at /api
)

# Initialize SQLAdmin
admin = create_admin(app)


# Fix for SQLAdmin static files with root_path
# Redirect /api/admin/statics/* to /admin/statics/*
@app.api_route("/api/admin/statics/{file_path:path}", methods=["GET", "HEAD"])
async def redirect_admin_statics(file_path: str):
    """Redirect SQLAdmin static files to correct path"""
    return RedirectResponse(url=f"/admin/statics/{file_path}", status_code=301)


@app.get("/")
def root():
    return {"message": "LAMFO API is running", "status": "operational"}


@app.get("/health")
def health_check():
    """Health check endpoint for Docker Swarm"""
    try:
        # Try to get a database connection
        db = next(get_db())
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "test_mode": os.getenv("TEST_MODE", "false").lower() == "true"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return Response(
            content={"status": "unhealthy", "error": str(e)},
            status_code=200  # Still return 200 to prevent container restarts
        )


@app.get("/members/", response_model=List[schemas.Member])
def read_members(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        members = crud.get_members(db, skip=skip, limit=limit)
        return members
    except Exception as e:
        logger.error(f"Error fetching members: {e}")
        # Return an empty list instead of failing
        return []


@app.get("/members/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    member = crud.get_member(db, member_id=member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@app.put("/members/{member_id}", response_model=schemas.Member)
def update_member(
    member_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db)
):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.update_member(db=db, member_id=member_id, member=member)


@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    crud.delete_member(db=db, member_id=member_id)
    return {"message": "Member deleted successfully"}


@app.post("/members/", response_model=schemas.Member, status_code=201)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = crud.get_member_by_email(db, email=member.email)
    if db_member:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_member(db=db, member=member)


@app.get("/projects/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)
):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.update_project(db=db, project_id=project_id, project=project)


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    crud.delete_project(db=db, project_id=project_id)
    return {"message": "Project deleted successfully"}


@app.post("/projects/", response_model=schemas.Project, status_code=201)
def create_project(
    project: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    return crud.create_project(db=db, project=project)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
