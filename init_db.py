"""Database initialization script for Billionaires application."""
import sqlite3
import os

def init_database(db_path='billionaires.db'):
    """Initialize the database with schema and sample data using recreate_database.sql."""
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute the normalized schema from recreate_database.sql
    try:
        with open('recreate_database.sql', 'r') as f:
            schema = f.read()
            cursor.executescript(schema)
        print(f"Database '{db_path}' initialized successfully with normalized schema and sample data!")
    except FileNotFoundError:
        print("Error: recreate_database.sql not found. Please ensure the file exists.")
        conn.close()
        return
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
