"""
Create COUNTRY table with proper foreign key to ECONOMICS.
Includes NULL checks for foreign key lookups.
"""
import sqlite3


def make_country(conn):
    """Create and populate the COUNTRY table."""
    cursor = conn.cursor()
    
    # Create COUNTRY table with proper data types and foreign key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS COUNTRY (
            id INTEGER PRIMARY KEY,
            countryName TEXT NOT NULL,
            grossTertiaryEducation REAL,
            grossPrimaryEducation REAL,
            lifeExpectancy REAL,
            population INTEGER,
            latitude REAL,
            longitude REAL,
            economics INTEGER,
            FOREIGN KEY (economics) REFERENCES ECONOMICS(id)
        )
    ''')
    
    # Sample country data with economic references
    country_data = [
        ('United States', 88.2, 101.5, 78.9, 331002651, 37.09024, -95.712891, 1),
        ('France', 65.9, 102.3, 82.7, 65273511, 46.227638, 2.213749, 2),
        ('China', 51.0, 104.2, 76.9, 1439323776, 35.86166, 104.195397, 3),
        ('India', 28.1, 112.8, 69.7, 1380004385, 20.593684, 78.96288, 4),
        ('Mexico', 38.4, 104.8, 75.1, 128932753, 23.634501, -102.552784, 5),
        ('United Kingdom', 60.0, 106.5, 81.3, 67886011, 55.378051, -3.435973, 6),
        ('Spain', 89.5, 105.2, 83.6, 46754778, 40.463667, -3.74922, 7),
        ('Italy', 63.8, 101.1, 83.5, 60461826, 41.87194, 12.56738, 8),
        ('Canada', 71.3, 101.8, 82.3, 37742154, 56.130366, -106.346771, 9),
        ('Brazil', 51.3, 107.2, 75.9, 212559417, -14.235004, -51.92528, 10),
    ]
    
    # Insert countries with NULL check for economics foreign key
    for country in country_data:
        countryName, grossTertiary, grossPrimary, lifeExpect, pop, lat, lon, econ_ref = country
        
        # NULL check: verify economics_id exists before inserting
        cursor.execute('SELECT id FROM ECONOMICS WHERE id = ?', (econ_ref,))
        economics_id = cursor.fetchone()
        
        if economics_id is None:
            # If economics record doesn't exist, use NULL for foreign key
            print(f"⚠️  Warning: Economics ID {econ_ref} not found for {countryName}, using NULL")
            econ_ref = None
        
        cursor.execute('''
            INSERT INTO COUNTRY (countryName, grossTertiaryEducation, grossPrimaryEducation,
                               lifeExpectancy, population, latitude, longitude, economics)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (countryName, grossTertiary, grossPrimary, lifeExpect, pop, lat, lon, econ_ref))
    
    conn.commit()
    print(f"✓ COUNTRY table created with {len(country_data)} records")


if __name__ == '__main__':
    # Test the function
    conn = sqlite3.connect('b.db')
    make_country(conn)
    conn.close()
