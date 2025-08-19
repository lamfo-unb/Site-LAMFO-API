
# LAMFO AI API Backend

This directory contains the backend API for the LAMFO website, built with FastAPI and SQLAlchemy. It provides endpoints and database models for managing LAMFO members, projects, and related data.

## Purpose

This backend serves as the core API for the LAMFO group, supporting member and project management, and is designed for easy integration with both development (SQLite) and production (PostgreSQL) databases.

## Structure

- `app/` — Main application code (FastAPI app, models, schemas, CRUD, database setup)
- `tests/` — Unit tests using pytest and SQLite for isolation
- `requirements.txt` — Main dependencies
- `requirements-test.txt` — Test dependencies
- `docker-compose.yml` — (Optional) For running with Docker
- `alembic.ini`, `pyproject.toml`, etc. — Configuration files

## Usage

1. Install dependencies:
	```sh
	pip install -r requirements.txt
	```
2. Run the API (development):
	```sh
	uvicorn app.main:app --reload
	```
3. Run tests:
	```sh
	pytest
	```

## Testing

- All tests use a temporary SQLite database for isolation.
- When integrating with PostgreSQL, add integration tests as needed.

## Notes

- The API docs are available at `/docs` when running the server.
- See `app/populate_db.py` for mock data generation.

---
For questions or contributions, contact the LAMFO team.
