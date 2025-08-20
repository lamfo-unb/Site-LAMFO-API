#!/usr/bin/env python
"""
Script to check the connection to the PostgreSQL database.
Run this script to test the database connection.
"""
import sys
from sqlalchemy import create_engine, text
from app.database import settings


def check_db_connection():
    """Test the database connection using settings from the environment."""
    try:
        print(f"Attempting to connect to database at: {settings.database_url}")
        engine = create_engine(settings.database_url)
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection successful!")
            
            # Get database information
            result = connection.execute(
                text("SELECT current_database(), current_user")
            )
            db_info = result.fetchone()
            print(f"Connected to database: {db_info[0]} as user: {db_info[1]}")
            
            # Get table list
            result = connection.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"Available tables: {', '.join(tables)}")
            else:
                print("No tables found in the database.")
            
            return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False


if __name__ == "__main__":
    success = check_db_connection()
    sys.exit(0 if success else 1)
