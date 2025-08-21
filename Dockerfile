FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including PostgreSQL client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
# SQLite fallback for development
ENV SQLITE_URL=sqlite:///./test.db
# Ensure we're not in test mode by default
ENV TEST_MODE=false

# Create empty SQLite database
RUN touch /app/test.db

# Expose the port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
