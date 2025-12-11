"""
Create PERSONAL_INFO table with proper schema.
This table stores personal information about billionaires.
"""
import sqlite3


def make_personal(conn):
    """Create and populate the PERSONAL_INFO table."""
    cursor = conn.cursor()
    
    # Create PERSONAL_INFO table with proper INTEGER PRIMARY KEY (not INTERGER)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PERSONAL_INFO (
            id INTEGER PRIMARY KEY,
            age INTEGER,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            birthDate TEXT,
            birthDay INTEGER,
            birthMonth INTEGER,
            birthYear INTEGER,
            gender TEXT,
            countryOfCitizenship TEXT
        )
    ''')
    
    # Sample personal info data
    personal_data = [
        (1, 57, 'Jeff', 'Bezos', '1964-01-12', 12, 1, 1964, 'M', 'United States'),
        (2, 50, 'Elon', 'Musk', '1971-06-28', 28, 6, 1971, 'M', 'United States'),
        (3, 72, 'Bernard', 'Arnault', '1949-03-05', 5, 3, 1949, 'M', 'France'),
        (4, 66, 'Bill', 'Gates', '1955-10-28', 28, 10, 1955, 'M', 'United States'),
        (5, 37, 'Mark', 'Zuckerberg', '1984-05-14', 14, 5, 1984, 'M', 'United States'),
        (6, 91, 'Warren', 'Buffett', '1930-08-30', 30, 8, 1930, 'M', 'United States'),
        (7, 64, 'Mukesh', 'Ambani', '1957-04-19', 19, 4, 1957, 'M', 'India'),
        (8, 81, 'Carlos', 'Slim Helu', '1940-01-28', 28, 1, 1940, 'M', 'Mexico'),
        (9, 48, 'Larry', 'Page', '1973-03-26', 26, 3, 1973, 'M', 'United States'),
        (10, 48, 'Sergey', 'Brin', '1973-08-21', 21, 8, 1973, 'M', 'United States'),
    ]
    
    cursor.executemany('''
        INSERT INTO PERSONAL_INFO (id, age, firstName, lastName, birthDate, birthDay, 
                                  birthMonth, birthYear, gender, countryOfCitizenship)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', personal_data)
    
    conn.commit()
    print(f"✓ PERSONAL_INFO table created with {len(personal_data)} records")


if __name__ == '__main__':
    # Test the function
    conn = sqlite3.connect('b.db')
    make_personal(conn)
    conn.close()
