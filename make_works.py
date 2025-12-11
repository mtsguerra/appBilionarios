"""
Create WORKS junction table with proper foreign keys.
Includes NULL checks for foreign key lookups.
"""
import sqlite3


def make_works(conn):
    """Create and populate the WORKS junction table."""
    cursor = conn.cursor()
    
    # Create WORKS table with proper foreign key constraints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WORKS (
            id INTEGER PRIMARY KEY,
            billionaire_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            title TEXT,
            FOREIGN KEY (billionaire_id) REFERENCES BILLIONARIES(id),
            FOREIGN KEY (company_id) REFERENCES COMPANY(id)
        )
    ''')
    
    # Sample works data (links billionaires to companies)
    # Format: (id, billionaire_id, company_id, title)
    works_data = [
        (1, 1, 1, 'CEO and Founder'),
        (2, 2, 3, 'CEO and Product Architect'),
        (3, 3, 4, 'Chairman and CEO'),
        (4, 4, 2, 'Co-Founder and Former CEO'),
        (5, 5, 8, 'Chairman and CEO'),
        (6, 6, 5, 'Chairman and CEO'),
        (7, 7, 6, 'Chairman and Managing Director'),
        (8, 8, 7, 'Chairman'),
        (9, 9, 9, 'Co-Founder'),
        (10, 10, 9, 'Co-Founder'),
    ]
    
    # Insert works with NULL checks for foreign keys
    for work in works_data:
        work_id, billionaire_id, company_id, title = work
        
        # NULL check: verify billionaire_id exists
        cursor.execute('SELECT id FROM BILLIONARIES WHERE id = ?', (billionaire_id,))
        billionaire_result = cursor.fetchone()
        
        if billionaire_result is None:
            print(f"⚠️  Warning: Billionaire ID {billionaire_id} not found, skipping work record")
            continue
        
        # NULL check: verify company_id exists
        cursor.execute('SELECT id FROM COMPANY WHERE id = ?', (company_id,))
        company_result = cursor.fetchone()
        
        if company_result is None:
            print(f"⚠️  Warning: Company ID {company_id} not found, skipping work record")
            continue
        
        cursor.execute('''
            INSERT INTO WORKS (id, billionaire_id, company_id, title)
            VALUES (?, ?, ?, ?)
        ''', (work_id, billionaire_id, company_id, title))
    
    conn.commit()
    print(f"✓ WORKS table created with {len(works_data)} records")


if __name__ == '__main__':
    # Test the function
    conn = sqlite3.connect('b.db')
    make_works(conn)
    conn.close()
