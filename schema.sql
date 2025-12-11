-- Schema for Billionaire Database Application

-- Drop existing tables if they exist
DROP TABLE IF EXISTS COUNTRYECONOMY;
DROP TABLE IF EXISTS COUNTRY;
DROP TABLE IF EXISTS CITY;
DROP TABLE IF EXISTS COMPANY;
DROP TABLE IF EXISTS PERSONAL;
DROP TABLE IF EXISTS BILLIONAIRE;

-- BILLIONAIRE table
CREATE TABLE BILLIONAIRE (
    rank INTEGER PRIMARY KEY,
    personName TEXT NOT NULL,
    selfMade INTEGER,  -- 0 for False, 1 for True
    status TEXT,
    cityName TEXT,
    source TEXT,
    finalWorth REAL,
    title TEXT,
    FOREIGN KEY (cityName) REFERENCES CITY(cityName),
    FOREIGN KEY (source) REFERENCES COMPANY(source)
);

-- PERSONAL table
CREATE TABLE PERSONAL (
    rank INTEGER PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    birthDate TEXT,
    birthDay INTEGER,
    birthMonth INTEGER,
    birthYear INTEGER,
    age INTEGER,
    gender TEXT,
    countryOfCitizenship TEXT,
    FOREIGN KEY (rank) REFERENCES BILLIONAIRE(rank),
    FOREIGN KEY (countryOfCitizenship) REFERENCES COUNTRY(countryName)
);

-- COMPANY table
CREATE TABLE COMPANY (
    source TEXT PRIMARY KEY,
    organization TEXT,
    category TEXT,
    industries TEXT
);

-- CITY table
CREATE TABLE CITY (
    cityName TEXT PRIMARY KEY,
    state TEXT,
    residenceStateRegion TEXT
);

-- COUNTRY table
CREATE TABLE COUNTRY (
    countryName TEXT PRIMARY KEY,
    lifeExpectancy REAL,
    grossTertiaryEducation REAL,
    grossPrimaryEducation REAL,
    population INTEGER,
    latitude REAL,
    longitude REAL
);

-- COUNTRYECONOMY table
CREATE TABLE COUNTRYECONOMY (
    countryName TEXT PRIMARY KEY,
    cpi REAL,
    cpiChange REAL,
    taxRevenue REAL,
    totalTaxRate REAL,
    gdp REAL,
    FOREIGN KEY (countryName) REFERENCES COUNTRY(countryName)
);

-- Create indexes for better query performance
CREATE INDEX idx_billionaire_cityName ON BILLIONAIRE(cityName);
CREATE INDEX idx_billionaire_source ON BILLIONAIRE(source);
CREATE INDEX idx_billionaire_selfMade ON BILLIONAIRE(selfMade);
CREATE INDEX idx_personal_countryOfCitizenship ON PERSONAL(countryOfCitizenship);
CREATE INDEX idx_personal_gender ON PERSONAL(gender);
CREATE INDEX idx_company_category ON COMPANY(category);
