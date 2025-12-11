"""
Create ECONOMICS table with proper schema.
This table stores economic indicators for countries.
"""
import sqlite3


def make_economics(conn):
    """Create and populate the ECONOMICS table."""
    cursor = conn.cursor()
    
    # Create ECONOMICS table with proper INTEGER PRIMARY KEY
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ECONOMICS (
            id INTEGER PRIMARY KEY,
            cpi REAL,
            cpiChange REAL,
            gdp REAL,
            taxRevenue REAL,
            totalTaxRate REAL
        )
    ''')
    
    # Insert sample economic data
    economics_data = [
        (1, 258.811, 4.7, 21427700000000, 25.6, 36.6),  # United States
        (2, 110.0, 1.1, 2715518000000, 46.2, 60.7),     # France
        (3, 107.0, 2.0, 14722730697890, 22.1, 59.2),    # China
        (4, 155.0, 6.2, 2875142000000, 17.7, 49.2),     # India
        (5, 107.0, 3.4, 1269956000000, 16.2, 51.7),     # Mexico
        (6, 106.0, 0.9, 2827113000000, 32.5, 30.0),     # United Kingdom
        (7, 103.5, 1.8, 1394116000000, 37.2, 47.0),     # Spain
        (8, 102.8, 1.2, 2003576000000, 42.4, 59.1),     # Italy
        (9, 141.6, 3.4, 1736426000000, 38.4, 20.8),     # Canada
        (10, 145.7, 4.5, 1839758000000, 32.3, 65.0),    # Brazil
    ]
    
    cursor.executemany('''
        INSERT INTO ECONOMICS (id, cpi, cpiChange, gdp, taxRevenue, totalTaxRate)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', economics_data)
    
    conn.commit()
    print(f"✓ ECONOMICS table created with {len(economics_data)} records")


if __name__ == '__main__':
    # Test the function
    conn = sqlite3.connect('b.db')
    make_economics(conn)
    conn.close()
