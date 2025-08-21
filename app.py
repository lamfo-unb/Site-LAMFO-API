"""
Minimal fallback application for LAMFO API
"""
from fastapi import FastAPI
import logging
import time

# Create a minimal FastAPI app
app = FastAPI(
    title="LAMFO API (Minimal Fallback)",
    description="Minimal fallback API when the main app fails to start"
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "LAMFO API Fallback is running",
        "status": "limited",
        "mode": "fallback",
        "info": "This is a minimal version of the API. The full version is currently unavailable."
    }

@app.get("/health")
def health():
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "mode": "fallback",
        "timestamp": time.time()
    }

@app.get("/members/")
def read_members():
    """Return a static list of members for fallback mode"""
    logger.info("Members endpoint accessed")
    return [
        {
            "id": 1,
            "name": "Sample Member 1",
            "email": "member1@example.com",
            "role": "Researcher",
            "bio": "This is a sample member for fallback mode"
        },
        {
            "id": 2,
            "name": "Sample Member 2",
            "email": "member2@example.com",
            "role": "Professor",
            "bio": "This is another sample member for fallback mode"
        }
    ]

@app.get("/projects/")
def read_projects():
    """Return a static list of projects for fallback mode"""
    logger.info("Projects endpoint accessed")
    return [
        {
            "id": 1,
            "title": "Sample Project 1",
            "description": "This is a sample project for fallback mode",
            "status": "Completed"
        },
        {
            "id": 2,
            "title": "Sample Project 2",
            "description": "This is another sample project for fallback mode",
            "status": "In Progress"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting fallback application directly")
    uvicorn.run(app, host="0.0.0.0", port=8000)
