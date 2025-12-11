"""
Create CITY table with proper foreign key to COUNTRY.
Includes NULL checks for foreign key lookups.
"""
import sqlite3


def make_city(conn):
    """Create and populate the CITY table."""
    cursor = conn.cursor()
    
    # Create CITY table with proper INTEGER type for country FK and foreign key constraint
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CITY (
            id INTEGER PRIMARY KEY,
            cityName TEXT NOT NULL,
            state TEXT,
            residenceStateRegion TEXT,
            country INTEGER,
            FOREIGN KEY (country) REFERENCES COUNTRY(id)
        )
    ''')
    
    # Sample city data with country references
    # Format: (cityName, state, residenceStateRegion, countryName_for_lookup)
    city_data = [
        ('New York', 'New York', 'Northeast', 'United States'),
        ('Seattle', 'Washington', 'Northwest', 'United States'),
        ('Omaha', 'Nebraska', 'Midwest', 'United States'),
        ('Los Angeles', 'California', 'West', 'United States'),
        ('Austin', 'Texas', 'South', 'United States'),
        ('Paris', 'Ile-de-France', 'Europe', 'France'),
        ('Hong Kong', 'Hong Kong', 'Asia', 'China'),
        ('Shanghai', 'Shanghai', 'Asia', 'China'),
        ('Mumbai', 'Maharashtra', 'Asia', 'India'),
        ('Mexico City', 'CDMX', 'Latin America', 'Mexico'),
        ('London', 'England', 'Europe', 'United Kingdom'),
        ('Madrid', 'Madrid', 'Europe', 'Spain'),
        ('Milan', 'Lombardy', 'Europe', 'Italy'),
        ('Toronto', 'Ontario', 'North America', 'Canada'),
        ('Sao Paulo', 'Sao Paulo', 'South America', 'Brazil'),
    ]
    
    # Insert cities with NULL check for country foreign key
    for city in city_data:
        cityName, state, region, countryName = city
        
        # NULL check: lookup country_id by name
        cursor.execute('SELECT id FROM COUNTRY WHERE countryName = ?', (countryName,))
        result = cursor.fetchone()
        
        if result is None:
            # If country doesn't exist, skip this city or use NULL
            print(f"⚠️  Warning: Country '{countryName}' not found for city '{cityName}', using NULL")
            country_id = None
        else:
            country_id = result[0]
        
        cursor.execute('''
            INSERT INTO CITY (cityName, state, residenceStateRegion, country)
            VALUES (?, ?, ?, ?)
        ''', (cityName, state, region, country_id))
    
    conn.commit()
    print(f"✓ CITY table created with {len(city_data)} records")


if __name__ == '__main__':
    # Test the function
    conn = sqlite3.connect('b.db')
    make_city(conn)
    conn.close()
