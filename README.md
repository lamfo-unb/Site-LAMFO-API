
# LAMFO AI API Backend

This directory contains the backend API for the LAMFO website, built with FastAPI and SQLAlchemy. It provides endpoints and database models for managing LAMFO members, projects, and related data.

## Purpose

This backend serves as the core API for the LAMFO group, supporting member and project management, and is designed for easy integration with both development (SQLite) and production (PostgreSQL) databases.

## Structure

- `app/` — Main application code (FastAPI app, models, schemas, CRUD, database setup)
- `tests/` — Unit tests using pytest and SQLite for isolation
- `requirements.txt` — Main dependencies
- `requirements-test.txt` — Test dependencies
- `docker-compose.yml` — For running with Docker and PostgreSQL
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

The project includes several test suites:

1. **Database Tests**: Test basic CRUD operations and database interactions
2. **API Tests**: Test the API endpoints for expected behavior 
3. **PostgreSQL Tests**: Integration tests with the PostgreSQL database (these are skipped if PostgreSQL is not available)

To run the tests:

```sh
# Run all tests
pytest

# Run specific test files
pytest tests/test_api.py
pytest tests/test_database.py
pytest tests/test_postgres.py

# Run with verbose output
pytest -v
```

## Docker Compose

The project includes a `docker-compose.yml` file for several reasons:

1. **Environment consistency**: Ensures the same environment across development and production
2. **Service orchestration**: Manages the API and database services together
3. **Dependency management**: Handles the dependency between the API and the database
4. **Volume management**: Manages persistent data storage for the database
5. **Network configuration**: Creates isolated networks for services
6. **Easy deployment**: Simplifies deployment with a single command

To use Docker Compose:

```sh
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Connecting to PostgreSQL

The API is configured to connect to a PostgreSQL database using the following environment variables:

- `POSTGRES_USER`: Database user (default: "lamfo")
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_HOST`: Database host (default: "database.1.uyp0svq7o4zphkxe880tjqkjd")
- `POSTGRES_PORT`: Database port (default: "5432")
- `POSTGRES_DB`: Database name (default: "lamfo_db")

These can be set in the `.env` file or passed as environment variables.

To check database connectivity, run:

```sh
python check_db.py
```

## Notes

- The API docs are available at `/docs` when running the server.
- See `app/populate_db.py` for mock data generation.

---
For questions or contributions, contact the LAMFO team.
