"""
Script para criar um banco de dados b.db de exemplo para testes.
Este script cria a estrutura do banco b.db conforme especificado no problema.
"""
import sqlite3
import os

def create_sample_b_db():
    """Cria um banco de dados b.db de exemplo com a estrutura correta."""
    
    # Remove o banco se já existir
    if os.path.exists('b.db'):
        os.remove('b.db')
        print("Banco b.db existente removido.")
    
    # Conecta ao banco
    conn = sqlite3.connect('b.db')
    cursor = conn.cursor()
    
    # Ativa foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    print("Criando estrutura do banco b.db...")
    
    # Cria tabela ECONOMICS
    cursor.execute('''
        CREATE TABLE ECONOMICS (
            id INTEGER PRIMARY KEY,
            cpi REAL,
            cpiChange REAL,
            gdp REAL,
            taxRevenue REAL,
            totalTaxRate REAL
        )
    ''')
    print("✓ Tabela ECONOMICS criada")
    
    # Cria tabela COUNTRY
    cursor.execute('''
        CREATE TABLE COUNTRY (
            id INTEGER PRIMARY KEY,
            countryName TEXT,
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
    print("✓ Tabela COUNTRY criada")
    
    # Cria tabela CITY
    cursor.execute('''
        CREATE TABLE CITY (
            id INTEGER PRIMARY KEY,
            cityName TEXT NOT NULL,
            state TEXT,
            residenceStateRegion TEXT,
            country INTEGER,
            FOREIGN KEY (country) REFERENCES COUNTRY(id)
        )
    ''')
    print("✓ Tabela CITY criada")
    
    # Cria tabela PERSONAL_INFO
    cursor.execute('''
        CREATE TABLE PERSONAL_INFO (
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
    print("✓ Tabela PERSONAL_INFO criada")
    
    # Cria tabela COMPANY
    cursor.execute('''
        CREATE TABLE COMPANY (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            organization TEXT,
            category TEXT,
            industries TEXT
        )
    ''')
    print("✓ Tabela COMPANY criada")
    
    # Cria tabela BILLIONARIES
    cursor.execute('''
        CREATE TABLE BILLIONARIES (
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
    print("✓ Tabela BILLIONARIES criada")
    
    # Cria tabela WORKS
    cursor.execute('''
        CREATE TABLE WORKS (
            id INTEGER PRIMARY KEY,
            billionaire_id INTEGER,
            company_id INTEGER,
            title TEXT,
            FOREIGN KEY (billionaire_id) REFERENCES BILLIONARIES(id),
            FOREIGN KEY (company_id) REFERENCES COMPANY(id)
        )
    ''')
    print("✓ Tabela WORKS criada")
    
    print("\nInserindo dados de exemplo...")
    
    # Insere ECONOMICS
    economics_data = [
        (1, 258.811, 4.7, 21427700000000, 25.6, 36.6),  # USA
        (2, 110.0, 1.1, 2715518000000, 46.2, 60.7),     # France
        (3, 107.0, 2.0, 14722730697890, 22.1, 59.2),    # China
        (4, 155.0, 6.2, 2875142000000, 17.7, 49.2),     # India
        (5, 107.0, 3.4, 1269956000000, 16.2, 51.7),     # Mexico
    ]
    cursor.executemany('INSERT INTO ECONOMICS VALUES (?, ?, ?, ?, ?, ?)', economics_data)
    print("✓ Dados de ECONOMICS inseridos")
    
    # Insere COUNTRY
    country_data = [
        (1, 'United States', 88.2, 101.5, 78.9, 331002651, 37.09024, -95.712891, 1),
        (2, 'France', 65.9, 102.3, 82.7, 65273511, 46.227638, 2.213749, 2),
        (3, 'China', 51.0, 104.2, 76.9, 1439323776, 35.86166, 104.195397, 3),
        (4, 'India', 28.1, 112.8, 69.7, 1380004385, 20.593684, 78.96288, 4),
        (5, 'Mexico', 38.4, 104.8, 75.1, 128932753, 23.634501, -102.552784, 5),
    ]
    cursor.executemany('INSERT INTO COUNTRY VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', country_data)
    print("✓ Dados de COUNTRY inseridos")
    
    # Insere CITY
    city_data = [
        (1, 'Seattle', 'Washington', 'Northwest', 1),
        (2, 'Austin', 'Texas', 'South', 1),
        (3, 'Paris', 'Ile-de-France', 'Europe', 2),
        (4, 'Los Angeles', 'California', 'West', 1),
        (5, 'New York', 'New York', 'Northeast', 1),
        (6, 'Mumbai', 'Maharashtra', 'Asia', 4),
        (7, 'Mexico City', 'CDMX', 'Latin America', 5),
        (8, 'Omaha', 'Nebraska', 'Midwest', 1),
    ]
    cursor.executemany('INSERT INTO CITY VALUES (?, ?, ?, ?, ?)', city_data)
    print("✓ Dados de CITY inseridos")
    
    # Insere PERSONAL_INFO
    personal_info_data = [
        (1, 59, 'Jeff', 'Bezos', '1964-01-12', 12, 1, 1964, 'M', 'United States'),
        (2, 52, 'Elon', 'Musk', '1971-06-28', 28, 6, 1971, 'M', 'United States'),
        (3, 74, 'Bernard', 'Arnault', '1949-03-05', 5, 3, 1949, 'M', 'France'),
        (4, 68, 'Bill', 'Gates', '1955-10-28', 28, 10, 1955, 'M', 'United States'),
        (5, 39, 'Mark', 'Zuckerberg', '1984-05-14', 14, 5, 1984, 'M', 'United States'),
        (6, 93, 'Warren', 'Buffett', '1930-08-30', 30, 8, 1930, 'M', 'United States'),
        (7, 66, 'Mukesh', 'Ambani', '1957-04-19', 19, 4, 1957, 'M', 'India'),
        (8, 83, 'Carlos', 'Slim Helu', '1940-01-28', 28, 1, 1940, 'M', 'Mexico'),
        (9, 50, 'Larry', 'Page', '1973-03-26', 26, 3, 1973, 'M', 'United States'),
        (10, 50, 'Sergey', 'Brin', '1973-08-21', 21, 8, 1973, 'M', 'United States'),
    ]
    cursor.executemany('INSERT INTO PERSONAL_INFO VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', personal_info_data)
    print("✓ Dados de PERSONAL_INFO inseridos")
    
    # Insere COMPANY
    company_data = [
        (1, 'Amazon', 'Amazon.com Inc.', 'Technology', 'E-commerce, Cloud Computing'),
        (2, 'Tesla, SpaceX', 'Tesla Inc., SpaceX', 'Automotive', 'Electric Vehicles, Aerospace'),
        (3, 'LVMH', 'LVMH Moët Hennessy Louis Vuitton', 'Fashion & Retail', 'Luxury Goods'),
        (4, 'Microsoft', 'Microsoft Corporation', 'Technology', 'Software, Cloud Computing'),
        (5, 'Facebook', 'Meta Platforms Inc.', 'Technology', 'Social Media, Internet'),
        (6, 'Berkshire Hathaway', 'Berkshire Hathaway Inc.', 'Finance & Investments', 'Diversified Holdings'),
        (7, 'Reliance Industries', 'Reliance Industries Limited', 'Diversified', 'Energy, Retail, Telecom'),
        (8, 'Grupo Carso', 'Grupo Carso S.A.B. de C.V.', 'Diversified', 'Industrial, Retail'),
        (9, 'Google', 'Alphabet Inc.', 'Technology', 'Internet, Software'),
    ]
    cursor.executemany('INSERT INTO COMPANY VALUES (?, ?, ?, ?, ?)', company_data)
    print("✓ Dados de COMPANY inseridos")
    
    # Insere BILLIONARIES
    billionaries_data = [
        (1, 1, 177000, 'Jeff Bezos', 1, 'D', 1, 1),
        (2, 2, 151000, 'Elon Musk', 1, 'D', 2, 2),
        (3, 3, 150000, 'Bernard Arnault', 1, 'D', 3, 3),
        (4, 4, 124000, 'Bill Gates', 1, 'D', 1, 4),
        (5, 5, 97000, 'Mark Zuckerberg', 1, 'D', 5, 5),
        (6, 6, 96000, 'Warren Buffett', 1, 'D', 8, 6),
        (7, 7, 84500, 'Mukesh Ambani', 1, 'D', 6, 7),
        (8, 8, 62800, 'Carlos Slim Helu', 1, 'D', 7, 8),
        (9, 9, 55000, 'Larry Page', 1, 'D', 4, 9),
        (10, 10, 53000, 'Sergey Brin', 1, 'D', 4, 10),
    ]
    cursor.executemany('INSERT INTO BILLIONARIES VALUES (?, ?, ?, ?, ?, ?, ?, ?)', billionaries_data)
    print("✓ Dados de BILLIONARIES inseridos")
    
    # Insere WORKS
    works_data = [
        (1, 1, 1, 'CEO and Founder'),
        (2, 2, 2, 'CEO and Product Architect'),
        (3, 3, 3, 'Chairman and CEO'),
        (4, 4, 4, 'Co-Founder and Former CEO'),
        (5, 5, 5, 'Chairman and CEO'),
        (6, 6, 6, 'Chairman and CEO'),
        (7, 7, 7, 'Chairman and Managing Director'),
        (8, 8, 8, 'Chairman'),
        (9, 9, 9, 'Co-Founder'),
        (10, 10, 9, 'Co-Founder'),
    ]
    cursor.executemany('INSERT INTO WORKS VALUES (?, ?, ?, ?)', works_data)
    print("✓ Dados de WORKS inseridos")
    
    # Commit e fecha conexão
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✓ Banco b.db criado com sucesso!")
    print("="*60)
    print("\nEstatísticas:")
    
    # Reabrir para contar
    conn = sqlite3.connect('b.db')
    cursor = conn.cursor()
    
    tables = ['ECONOMICS', 'COUNTRY', 'CITY', 'PERSONAL_INFO', 'COMPANY', 'BILLIONARIES', 'WORKS']
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"  - {table}: {count} registros")
    
    conn.close()
    
    print("\nO arquivo b.db está pronto para uso!")
    print("Execute: python app.py")

if __name__ == '__main__':
    create_sample_b_db()
