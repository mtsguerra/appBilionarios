"""
Main script to create the b.db database with proper schema.
Orchestrates the creation of all tables in the correct order to handle foreign key dependencies.
"""
import sqlite3
import os
from make_economics import make_economics
from make_country import make_country
from make_city import make_city
from make_personal import make_personal
from make_company import make_company
from make_billionaries import make_billionaries
from make_works import make_works


def create_b_db():
    """Create the b.db database with all tables and data."""
    db_path = 'b.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing {db_path}")
    
    # Connect to database and enable foreign key support
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    print("="*70)
    print("Creating b.db Database")
    print("="*70)
    print()
    
    try:
        # Create tables in correct order to handle foreign key dependencies
        # 1. Base tables first (no dependencies)
        print("Creating base tables...")
        make_economics(conn)
        make_personal(conn)
        make_company(conn)
        print()
        
        # 2. Tables that depend on base tables
        print("Creating dependent tables...")
        make_country(conn)      # depends on ECONOMICS
        make_city(conn)         # depends on COUNTRY
        print()
        
        # 3. Tables that depend on multiple other tables
        print("Creating main tables...")
        make_billionaries(conn) # depends on CITY and PERSONAL_INFO
        print()
        
        # 4. Junction tables last
        print("Creating junction tables...")
        make_works(conn)        # depends on BILLIONARIES and COMPANY
        print()
        
        print("="*70)
        print("✅ Database b.db created successfully!")
        print("="*70)
        print()
        print("To verify the database, run:")
        print("  python verificar_b_db.py")
        print()
        print("To start the application, run:")
        print("  python app.py")
        print()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    create_b_db()
