FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV POSTGRES_USER=lamfo
ENV POSTGRES_PASSWORD=TW6t68VwY8eS
ENV POSTGRES_HOST=database.1.uyp0svq7o4zphkxe880tjqkjd
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=lamfo_db

# Expose the port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
