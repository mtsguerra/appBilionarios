-- ============================================================================
-- Billionaires Database Recreation Script
-- ============================================================================
-- This script creates a normalized database schema for the Billionaires app
-- based on the provided ER diagram.
--
-- USAGE:
-- 1. To recreate the database from scratch:
--    sqlite3 billionaires.db < recreate_database.sql
--
-- 2. Or use Python:
--    python init_db.py
--
-- 3. The script includes sample data that can be modified or replaced
--    with actual data from your data sources.
--
-- STRUCTURE:
-- - COUNTRY: Base table for country information
-- - CITY: Cities with foreign key to COUNTRY
-- - COMPANY: Companies/organizations
-- - BILLIONARIES: Main billionaire table with FK to CITY
-- - WORKS: Junction table linking BILLIONARIES to COMPANY
-- ============================================================================

-- ============================================================================
-- DROP TABLES (in correct order to handle foreign key dependencies)
-- ============================================================================

-- Drop junction and dependent tables first
DROP TABLE IF EXISTS WORKS;
DROP TABLE IF EXISTS BILLIONARIES;

-- Drop intermediate tables
DROP TABLE IF EXISTS CITY;
DROP TABLE IF EXISTS COMPANY;

-- Drop base tables last
DROP TABLE IF EXISTS COUNTRY;

-- ============================================================================
-- CREATE TABLES (in correct order to handle foreign key dependencies)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- COUNTRY Table
-- Base table containing country-level information
-- ----------------------------------------------------------------------------
CREATE TABLE COUNTRY (
    id INTEGER PRIMARY KEY,
    countryName VARCHAR(50) NOT NULL,
    cpi DECIMAL(7,2),
    cpiChange DECIMAL(4,2),
    grossTertiaryEducation DECIMAL(4,2),
    grossPrimaryEducation DECIMAL(5,2),
    gdp DECIMAL(15,2),
    lifeExpectancy DECIMAL(4,2),
    taxRevenue DECIMAL(4,2),
    totalTaxRate DECIMAL(4,2),
    population INTEGER,
    latitude DECIMAL(11,8),
    longitude DECIMAL(11,8)
);

-- ----------------------------------------------------------------------------
-- CITY Table
-- Contains city information with foreign key relationship to COUNTRY
-- ----------------------------------------------------------------------------
CREATE TABLE CITY (
    id INTEGER PRIMARY KEY,
    cityName VARCHAR(50) NOT NULL,
    state VARCHAR(50),
    residenceStateRegion VARCHAR(20),
    country INTEGER NOT NULL,
    FOREIGN KEY (country) REFERENCES COUNTRY(id)
);

-- ----------------------------------------------------------------------------
-- COMPANY Table
-- Contains company/organization information
-- ----------------------------------------------------------------------------
CREATE TABLE COMPANY (
    id INTEGER PRIMARY KEY,
    source VARCHAR(40),
    organization VARCHAR(60),
    category VARCHAR(40),
    industr VARCHAR(40)
);

-- ----------------------------------------------------------------------------
-- BILLIONARIES Table
-- Main billionaire information with foreign key to CITY
-- Note: Uses "BILLIONARIES" spelling as per ER diagram
-- ----------------------------------------------------------------------------
CREATE TABLE BILLIONARIES (
    id INTEGER PRIMARY KEY,
    rank INTEGER,
    finalWorth DECIMAL(6,2),
    personName VARCHAR(60) NOT NULL,
    age INTEGER,
    firstName VARCHAR(15),
    lastName VARCHAR(15),
    birthDate VARCHAR(10),
    birthDay INTEGER,
    birthMonth INTEGER,
    birthYear INTEGER,
    gender VARCHAR(1),
    selfMade BOOLEAN,
    countryOfCitizenship VARCHAR(50),
    status VARCHAR(20),
    city INTEGER,
    FOREIGN KEY (city) REFERENCES CITY(id)
);

-- ----------------------------------------------------------------------------
-- WORKS Table
-- Junction table linking BILLIONARIES to COMPANY with additional title field
-- Represents the many-to-many relationship between billionaires and companies
-- ----------------------------------------------------------------------------
CREATE TABLE WORKS (
    id INTEGER PRIMARY KEY,
    billionaire_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    title VARCHAR(40),
    FOREIGN KEY (billionaire_id) REFERENCES BILLIONARIES(id),
    FOREIGN KEY (company_id) REFERENCES COMPANY(id)
);

-- ============================================================================
-- CREATE INDEXES for better query performance
-- ============================================================================

-- Indexes for foreign keys
CREATE INDEX idx_city_country ON CITY(country);
CREATE INDEX idx_billionaries_city ON BILLIONARIES(city);
CREATE INDEX idx_works_billionaire ON WORKS(billionaire_id);
CREATE INDEX idx_works_company ON WORKS(company_id);

-- Indexes for commonly queried fields
CREATE INDEX idx_billionaries_rank ON BILLIONARIES(rank);
CREATE INDEX idx_billionaries_gender ON BILLIONARIES(gender);
CREATE INDEX idx_billionaries_selfMade ON BILLIONARIES(selfMade);
CREATE INDEX idx_billionaries_country ON BILLIONARIES(countryOfCitizenship);
CREATE INDEX idx_company_category ON COMPANY(category);

-- ============================================================================
-- INSERT SAMPLE DATA
-- ============================================================================
-- This section contains sample data for testing.
-- Replace with actual data imports as needed.

-- ----------------------------------------------------------------------------
-- Insert COUNTRY data
-- ----------------------------------------------------------------------------
INSERT INTO COUNTRY (id, countryName, cpi, cpiChange, grossTertiaryEducation, grossPrimaryEducation, gdp, lifeExpectancy, taxRevenue, totalTaxRate, population, latitude, longitude) VALUES
(1, 'United States', 258.811, 4.7, 88.2, 101.5, 21427700000000, 78.9, 25.6, 36.6, 331002651, 37.09024, -95.712891),
(2, 'France', 110.0, 1.1, 65.9, 102.3, 2715518000000, 82.7, 46.2, 60.7, 65273511, 46.227638, 2.213749),
(3, 'China', 107.0, 2.0, 51.0, 104.2, 14722730697890, 76.9, 22.1, 59.2, 1439323776, 35.86166, 104.195397),
(4, 'India', 155.0, 6.2, 28.1, 112.8, 2875142000000, 69.7, 17.7, 49.2, 1380004385, 20.593684, 78.96288),
(5, 'Mexico', 107.0, 3.4, 38.4, 104.8, 1269956000000, 75.1, 16.2, 51.7, 128932753, 23.634501, -102.552784),
(6, 'United Kingdom', 106.0, 0.9, 60.0, 106.5, 2827113000000, 81.3, 32.5, 30.0, 67886011, 55.378051, -3.435973),
(7, 'Spain', 103.5, 1.8, 89.5, 105.2, 1394116000000, 83.6, 37.2, 47.0, 46754778, 40.463667, -3.74922),
(8, 'Italy', 102.8, 1.2, 63.8, 101.1, 2003576000000, 83.5, 42.4, 59.1, 60461826, 41.87194, 12.56738),
(9, 'Canada', 141.6, 3.4, 71.3, 101.8, 1736426000000, 82.3, 38.4, 20.8, 37742154, 56.130366, -106.346771),
(10, 'Brazil', 145.7, 4.5, 51.3, 107.2, 1839758000000, 75.9, 32.3, 65.0, 212559417, -14.235004, -51.92528);

-- ----------------------------------------------------------------------------
-- Insert CITY data
-- ----------------------------------------------------------------------------
INSERT INTO CITY (id, cityName, state, residenceStateRegion, country) VALUES
(1, 'New York', 'New York', 'Northeast', 1),
(2, 'Seattle', 'Washington', 'Northwest', 1),
(3, 'Omaha', 'Nebraska', 'Midwest', 1),
(4, 'Los Angeles', 'California', 'West', 1),
(5, 'Austin', 'Texas', 'South', 1),
(6, 'Paris', 'Ile-de-France', 'Europe', 2),
(7, 'Hong Kong', 'Hong Kong', 'Asia', 3),
(8, 'Shanghai', 'Shanghai', 'Asia', 3),
(9, 'Mumbai', 'Maharashtra', 'Asia', 4),
(10, 'Mexico City', 'CDMX', 'Latin America', 5),
(11, 'London', 'England', 'Europe', 6),
(12, 'Madrid', 'Madrid', 'Europe', 7),
(13, 'Milan', 'Lombardy', 'Europe', 8),
(14, 'Toronto', 'Ontario', 'North America', 9),
(15, 'Sao Paulo', 'Sao Paulo', 'South America', 10);

-- ----------------------------------------------------------------------------
-- Insert COMPANY data
-- ----------------------------------------------------------------------------
INSERT INTO COMPANY (id, source, organization, category, industr) VALUES
(1, 'Amazon', 'Amazon.com Inc.', 'Technology', 'E-commerce, Cloud Computing'),
(2, 'Microsoft', 'Microsoft Corporation', 'Technology', 'Software, Cloud Computing'),
(3, 'Tesla', 'Tesla Inc.', 'Automotive', 'Electric Vehicles, Clean Energy'),
(4, 'LVMH', 'LVMH Moët Hennessy Louis Vuitton', 'Fashion & Retail', 'Luxury Goods'),
(5, 'Berkshire Hathaway', 'Berkshire Hathaway Inc.', 'Finance & Investments', 'Diversified Holdings'),
(6, 'Reliance Industries', 'Reliance Industries Limited', 'Diversified', 'Energy, Retail, Telecom'),
(7, 'Grupo Carso', 'Grupo Carso S.A.B. de C.V.', 'Diversified', 'Industrial, Retail, Infrastructure'),
(8, 'Facebook', 'Meta Platforms Inc.', 'Technology', 'Social Media, Internet'),
(9, 'Google', 'Alphabet Inc.', 'Technology', 'Internet, Software'),
(10, 'Oracle', 'Oracle Corporation', 'Technology', 'Software, Cloud Computing');

-- ----------------------------------------------------------------------------
-- Insert BILLIONARIES data
-- ----------------------------------------------------------------------------
INSERT INTO BILLIONARIES (id, rank, finalWorth, personName, age, firstName, lastName, birthDate, birthDay, birthMonth, birthYear, gender, selfMade, countryOfCitizenship, status, city) VALUES
(1, 1, 177000, 'Jeff Bezos', 57, 'Jeff', 'Bezos', '1964-01-12', 12, 1, 1964, 'M', 1, 'United States', 'D', 2),
(2, 2, 151000, 'Elon Musk', 50, 'Elon', 'Musk', '1971-06-28', 28, 6, 1971, 'M', 1, 'United States', 'D', 5),
(3, 3, 150000, 'Bernard Arnault', 72, 'Bernard', 'Arnault', '1949-03-05', 5, 3, 1949, 'M', 1, 'France', 'D', 6),
(4, 4, 124000, 'Bill Gates', 66, 'Bill', 'Gates', '1955-10-28', 28, 10, 1955, 'M', 1, 'United States', 'D', 2),
(5, 5, 97000, 'Mark Zuckerberg', 37, 'Mark', 'Zuckerberg', '1984-05-14', 14, 5, 1984, 'M', 1, 'United States', 'D', 1),
(6, 6, 96000, 'Warren Buffett', 91, 'Warren', 'Buffett', '1930-08-30', 30, 8, 1930, 'M', 1, 'United States', 'D', 3),
(7, 7, 84500, 'Mukesh Ambani', 64, 'Mukesh', 'Ambani', '1957-04-19', 19, 4, 1957, 'M', 1, 'India', 'D', 9),
(8, 8, 62800, 'Carlos Slim Helu', 81, 'Carlos', 'Slim Helu', '1940-01-28', 28, 1, 1940, 'M', 1, 'Mexico', 'D', 10),
(9, 9, 55000, 'Larry Page', 48, 'Larry', 'Page', '1973-03-26', 26, 3, 1973, 'M', 1, 'United States', 'D', 4),
(10, 10, 53000, 'Sergey Brin', 48, 'Sergey', 'Brin', '1973-08-21', 21, 8, 1973, 'M', 1, 'United States', 'D', 4);

-- ----------------------------------------------------------------------------
-- Insert WORKS data (junction table)
-- Links billionaires to companies with their titles
-- ----------------------------------------------------------------------------
INSERT INTO WORKS (id, billionaire_id, company_id, title) VALUES
(1, 1, 1, 'CEO and Founder'),
(2, 2, 3, 'CEO and Product Architect'),
(3, 3, 4, 'Chairman and CEO'),
(4, 4, 2, 'Co-Founder and Former CEO'),
(5, 5, 8, 'Chairman and CEO'),
(6, 6, 5, 'Chairman and CEO'),
(7, 7, 6, 'Chairman and Managing Director'),
(8, 8, 7, 'Chairman'),
(9, 9, 9, 'Co-Founder'),
(10, 10, 9, 'Co-Founder');

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================
-- Uncomment these queries to verify the database structure after creation

-- Count records in each table
-- SELECT 'COUNTRY' as table_name, COUNT(*) as record_count FROM COUNTRY
-- UNION ALL SELECT 'CITY', COUNT(*) FROM CITY
-- UNION ALL SELECT 'COMPANY', COUNT(*) FROM COMPANY
-- UNION ALL SELECT 'BILLIONARIES', COUNT(*) FROM BILLIONARIES
-- UNION ALL SELECT 'WORKS', COUNT(*) FROM WORKS;

-- Sample join query to verify relationships
-- SELECT 
--     b.personName, b.rank, b.finalWorth,
--     c.cityName, c.state,
--     co.countryName,
--     comp.organization, w.title
-- FROM BILLIONARIES b
-- LEFT JOIN CITY c ON b.city = c.id
-- LEFT JOIN COUNTRY co ON c.country = co.id
-- LEFT JOIN WORKS w ON b.id = w.billionaire_id
-- LEFT JOIN COMPANY comp ON w.company_id = comp.id
-- ORDER BY b.rank
-- LIMIT 10;

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
