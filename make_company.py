"""
Create COMPANY table with proper schema.
This table stores company/organization information.
"""
import sqlite3


def make_company(conn):
    """Create and populate the COMPANY table."""
    cursor = conn.cursor()
    
    # Create COMPANY table with proper schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS COMPANY (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            organization TEXT,
            category TEXT,
            industries TEXT
        )
    ''')
    
    # Sample company data
    company_data = [
        (1, 'Amazon', 'Amazon.com Inc.', 'Technology', 'E-commerce, Cloud Computing'),
        (2, 'Microsoft', 'Microsoft Corporation', 'Technology', 'Software, Cloud Computing'),
        (3, 'Tesla', 'Tesla Inc.', 'Automotive', 'Electric Vehicles, Clean Energy'),
        (4, 'LVMH', 'LVMH Moët Hennessy Louis Vuitton', 'Fashion & Retail', 'Luxury Goods'),
        (5, 'Berkshire Hathaway', 'Berkshire Hathaway Inc.', 'Finance & Investments', 'Diversified Holdings'),
        (6, 'Reliance Industries', 'Reliance Industries Limited', 'Diversified', 'Energy, Retail, Telecom'),
        (7, 'Grupo Carso', 'Grupo Carso S.A.B. de C.V.', 'Diversified', 'Industrial, Retail, Infrastructure'),
        (8, 'Facebook', 'Meta Platforms Inc.', 'Technology', 'Social Media, Internet'),
        (9, 'Google', 'Alphabet Inc.', 'Technology', 'Internet, Software'),
        (10, 'Oracle', 'Oracle Corporation', 'Technology', 'Software, Cloud Computing'),
    ]
    
    cursor.executemany('''
        INSERT INTO COMPANY (id, source, organization, category, industries)
        VALUES (?, ?, ?, ?, ?)
    ''', company_data)
    
    conn.commit()
    print(f"✓ COMPANY table created with {len(company_data)} records")


if __name__ == '__main__':
    # Test the function
    conn = sqlite3.connect('b.db')
    make_company(conn)
    conn.close()
