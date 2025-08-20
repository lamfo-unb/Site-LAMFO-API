from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from . import models, schemas, crud
from .database import engine, get_db

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create a FastAPI app
app = FastAPI(
    title="LAMFO API",
    description="API for managing LAMFO members and projects"
)


@app.get("/")
def root():
    return {"message": "LAMFO API is running", "status": "operational"}


@app.get("/members/", response_model=List[schemas.Member])
def read_members(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    members = crud.get_members(db, skip=skip, limit=limit)
    return members


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
