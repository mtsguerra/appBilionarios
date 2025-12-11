"""
Create BILLIONARIES table with proper foreign keys.
Includes NULL checks for foreign key lookups.
"""
import sqlite3


def make_billionaries(conn):
    """Create and populate the BILLIONARIES table."""
    cursor = conn.cursor()
    
    # Create BILLIONARIES table with proper INTEGER types and foreign key constraints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BILLIONARIES (
            id INTEGER PRIMARY KEY,
            rank INTEGER NOT NULL,
            finalWorth REAL NOT NULL,
            personName TEXT NOT NULL,
            selfMade INTEGER,
            status TEXT,
            city INTEGER,
            personalInfo INTEGER,
            FOREIGN KEY (city) REFERENCES CITY(id),
            FOREIGN KEY (personalInfo) REFERENCES PERSONAL_INFO(id)
        )
    ''')
    
    # Sample billionaire data
    # Format: (id, rank, finalWorth, personName, selfMade, status, cityName_for_lookup, personal_id)
    billionaire_data = [
        (1, 1, 177000, 'Jeff Bezos', 1, 'D', 'Seattle', 1),
        (2, 2, 151000, 'Elon Musk', 1, 'D', 'Austin', 2),
        (3, 3, 150000, 'Bernard Arnault', 1, 'D', 'Paris', 3),
        (4, 4, 124000, 'Bill Gates', 1, 'D', 'Seattle', 4),
        (5, 5, 97000, 'Mark Zuckerberg', 1, 'D', 'New York', 5),
        (6, 6, 96000, 'Warren Buffett', 1, 'D', 'Omaha', 6),
        (7, 7, 84500, 'Mukesh Ambani', 1, 'D', 'Mumbai', 7),
        (8, 8, 62800, 'Carlos Slim Helu', 1, 'D', 'Mexico City', 8),
        (9, 9, 55000, 'Larry Page', 1, 'D', 'Los Angeles', 9),
        (10, 10, 53000, 'Sergey Brin', 1, 'D', 'Los Angeles', 10),
    ]
    
    # Insert billionaires with NULL checks for foreign keys
    for billionaire in billionaire_data:
        bid, rank, worth, name, selfMade, status, cityName, personal_id = billionaire
        
        # NULL check: lookup city_id by name
        cursor.execute('SELECT id FROM CITY WHERE cityName = ?', (cityName,))
        city_result = cursor.fetchone()
        
        if city_result is None:
            print(f"⚠️  Warning: City '{cityName}' not found for {name}, using NULL")
            city_id = None
        else:
            city_id = city_result[0]
        
        # NULL check: verify personal_id exists
        cursor.execute('SELECT id FROM PERSONAL_INFO WHERE id = ?', (personal_id,))
        personal_result = cursor.fetchone()
        
        if personal_result is None:
            print(f"⚠️  Warning: Personal info ID {personal_id} not found for {name}, using NULL")
            personal_id = None
        
        cursor.execute('''
            INSERT INTO BILLIONARIES (id, rank, finalWorth, personName, selfMade, status, city, personalInfo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bid, rank, worth, name, selfMade, status, city_id, personal_id))
    
    conn.commit()
    print(f"✓ BILLIONARIES table created with {len(billionaire_data)} records")


if __name__ == '__main__':
    # Test the function
    conn = sqlite3.connect('b.db')
    make_billionaries(conn)
    conn.close()
