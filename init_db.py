"""Script de inicialização do banco de dados para aplicação de Bilionários."""
import sqlite3
import os

def init_database(db_path='billionaires.db'):
    """Inicializar o banco de dados com schema e dados de exemplo."""
    
    # Remover banco existente se existir
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ler e executar schema
    with open('schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    # Inserir dados de exemplo
    
    # Dados de exemplo de CITY
    cities = [
        ('New York', 'New York', 'Northeast'),
        ('Paris', 'Ile-de-France', 'Europe'),
        ('Hong Kong', 'Hong Kong', 'Asia'),
        ('Seattle', 'Washington', 'Northwest'),
        ('Omaha', 'Nebraska', 'Midwest'),
        ('Mumbai', 'Maharashtra', 'Asia'),
        ('Mexico City', 'CDMX', 'Latin America'),
        ('London', 'England', 'Europe'),
    ]
    cursor.executemany('INSERT INTO CITY (cityName, state, residenceStateRegion) VALUES (?, ?, ?)', cities)
    
    # Dados de exemplo de COUNTRY
    countries = [
        ('United States', 78.9, 88.2, 101.5, 331002651, 37.09024, -95.712891),
        ('France', 82.7, 65.9, 102.3, 65273511, 46.227638, 2.213749),
        ('China', 76.9, 51.0, 104.2, 1439323776, 35.86166, 104.195397),
        ('India', 69.7, 28.1, 112.8, 1380004385, 20.593684, 78.96288),
        ('Mexico', 75.1, 38.4, 104.8, 128932753, 23.634501, -102.552784),
        ('United Kingdom', 81.3, 60.0, 106.5, 67886011, 55.378051, -3.435973),
    ]
    cursor.executemany(
        'INSERT INTO COUNTRY (countryName, lifeExpectancy, grossTertiaryEducation, grossPrimaryEducation, population, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)',
        countries
    )
    
    # Dados de exemplo de COUNTRYECONOMY
    economies = [
        ('United States', 258.811, 4.7, 25.6, 36.6, 21427700000000),
        ('France', 110.0, 1.1, 46.2, 60.7, 2715518000000),
        ('China', 107.0, 2.0, 22.1, 59.2, 14722730697890),
        ('India', 155.0, 6.2, 17.7, 49.2, 2875142000000),
        ('Mexico', 107.0, 3.4, 16.2, 51.7, 1269956000000),
        ('United Kingdom', 106.0, 0.9, 32.5, 30.0, 2827113000000),
    ]
    cursor.executemany(
        'INSERT INTO COUNTRYECONOMY (countryName, cpi, cpiChange, taxRevenue, totalTaxRate, gdp) VALUES (?, ?, ?, ?, ?, ?)',
        economies
    )
    
    # Dados de exemplo de COMPANY
    companies = [
        ('Amazon', 'Amazon.com Inc.', 'Technology', 'E-commerce, Cloud Computing'),
        ('Microsoft', 'Microsoft Corporation', 'Technology', 'Software, Cloud Computing'),
        ('Tesla', 'Tesla Inc.', 'Automotive', 'Electric Vehicles, Clean Energy'),
        ('LVMH', 'LVMH Moët Hennessy Louis Vuitton', 'Fashion & Retail', 'Luxury Goods'),
        ('Berkshire Hathaway', 'Berkshire Hathaway Inc.', 'Finance & Investments', 'Diversified Holdings'),
        ('Reliance Industries', 'Reliance Industries Limited', 'Diversified', 'Energy, Retail, Telecom'),
        ('Grupo Carso', 'Grupo Carso S.A.B. de C.V.', 'Diversified', 'Industrial, Retail, Infrastructure'),
        ('Facebook', 'Meta Platforms Inc.', 'Technology', 'Social Media, Internet'),
    ]
    cursor.executemany(
        'INSERT INTO COMPANY (source, organization, category, industries) VALUES (?, ?, ?, ?)',
        companies
    )
    
    # Dados de exemplo de BILLIONAIRE
    billionaires = [
        (1, 'Jeff Bezos', 1, 'D', 'Seattle', 'Amazon', 177000.0, 'CEO'),
        (2, 'Elon Musk', 1, 'D', 'Seattle', 'Tesla', 151000.0, 'CEO'),
        (3, 'Bernard Arnault', 1, 'D', 'Paris', 'LVMH', 150000.0, 'CEO'),
        (4, 'Bill Gates', 1, 'D', 'Seattle', 'Microsoft', 124000.0, 'Co-Founder'),
        (5, 'Mark Zuckerberg', 1, 'D', 'New York', 'Facebook', 97000.0, 'CEO'),
        (6, 'Warren Buffett', 1, 'D', 'Omaha', 'Berkshire Hathaway', 96000.0, 'CEO'),
        (7, 'Mukesh Ambani', 1, 'D', 'Mumbai', 'Reliance Industries', 84500.0, 'Chairman'),
        (8, 'Carlos Slim Helu', 1, 'D', 'Mexico City', 'Grupo Carso', 62800.0, 'Chairman'),
    ]
    cursor.executemany(
        'INSERT INTO BILLIONAIRE (rank, personName, selfMade, status, cityName, source, finalWorth, title) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        billionaires
    )
    
    # Dados de exemplo de PERSONAL
    personals = [
        (1, 'Jeff', 'Bezos', '1964-01-12', 12, 1, 1964, 57, 'M', 'United States'),
        (2, 'Elon', 'Musk', '1971-06-28', 28, 6, 1971, 50, 'M', 'United States'),
        (3, 'Bernard', 'Arnault', '1949-03-05', 5, 3, 1949, 72, 'M', 'France'),
        (4, 'Bill', 'Gates', '1955-10-28', 28, 10, 1955, 66, 'M', 'United States'),
        (5, 'Mark', 'Zuckerberg', '1984-05-14', 14, 5, 1984, 37, 'M', 'United States'),
        (6, 'Warren', 'Buffett', '1930-08-30', 30, 8, 1930, 91, 'M', 'United States'),
        (7, 'Mukesh', 'Ambani', '1957-04-19', 19, 4, 1957, 64, 'M', 'India'),
        (8, 'Carlos', 'Slim Helu', '1940-01-28', 28, 1, 1940, 81, 'M', 'Mexico'),
    ]
    cursor.executemany(
        'INSERT INTO PERSONAL (rank, firstName, lastName, birthDate, birthDay, birthMonth, birthYear, age, gender, countryOfCitizenship) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        personals
    )
    
    conn.commit()
    conn.close()
    
    print(f"Banco de dados '{db_path}' inicializado com sucesso com dados de exemplo!")

if __name__ == '__main__':
    init_database()
