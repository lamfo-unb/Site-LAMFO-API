from fastapi import FastAPI, HTTPException
import uvicorn

# Create a minimal FastAPI app
app = FastAPI(title="LAMFO API", description="API for managing LAMFO members and projects")

# Sample data
sample_members = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "Data Scientist"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "Researcher"}
]

sample_projects = [
    {"id": 1, "title": "AI Research", "description": "Research on advanced AI models", "status": "active"},
    {"id": 2, "title": "Data Analysis", "description": "Analysis of economic data", "status": "completed"}
]

# Health check
@app.get("/")
def root():
    return {"message": "LAMFO API is running", "status": "operational"}

# Member endpoints
@app.get("/members/")
def read_members(skip: int = 0, limit: int = 100):
    end = min(skip + limit, len(sample_members))
    return sample_members[skip:end]

@app.get("/members/{member_id}")
def read_member(member_id: int):
    for member in sample_members:
        if member["id"] == member_id:
            return member
    raise HTTPException(status_code=404, detail="Member not found")

# Project endpoints
@app.get("/projects/")
def read_projects(skip: int = 0, limit: int = 100):
    end = min(skip + limit, len(sample_projects))
    return sample_projects[skip:end]

@app.get("/projects/{project_id}")
def read_project(project_id: int):
    for project in sample_projects:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
