# Database Creation Scripts

This directory contains Python scripts to create and populate the `b.db` database for the Billionaires application.

## Overview

The database creation scripts are designed to create a properly normalized database with:
- ✅ Correct data types (INTEGER, TEXT, REAL)
- ✅ Proper foreign key constraints
- ✅ NULL checks to prevent crashes during data population
- ✅ Sample data for testing

## Scripts

### Main Script
- **`create_b_db.py`** - Main orchestration script that creates the entire database

### Individual Table Scripts (executed in dependency order)

#### Base Tables (no dependencies)
1. **`make_economics.py`** - Creates ECONOMICS table with economic indicators
2. **`make_personal.py`** - Creates PERSONAL_INFO table with biographical data
3. **`make_company.py`** - Creates COMPANY table with organization data

#### Dependent Tables
4. **`make_country.py`** - Creates COUNTRY table (depends on ECONOMICS)
5. **`make_city.py`** - Creates CITY table (depends on COUNTRY)

#### Main Tables
6. **`make_billionaries.py`** - Creates BILLIONARIES table (depends on CITY and PERSONAL_INFO)

#### Junction Tables
7. **`make_works.py`** - Creates WORKS junction table (links BILLIONARIES and COMPANY)

## Usage

### Quick Start

To create the database from scratch:

```bash
python create_b_db.py
```

This will:
1. Remove any existing `b.db` file
2. Create all tables in the correct order
3. Populate tables with sample data
4. Print a success message

### Verify the Database

After creation, verify the database structure:

```bash
python verificar_b_db.py
```

This will check:
- All tables exist
- All required columns are present
- Data is populated correctly
- JOINs work properly

### Run the Application

Start the Flask application:

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

## Database Schema

### Tables and Relationships

```
ECONOMICS (id)
    ↑
    |
COUNTRY (id, economics FK)
    ↑
    |
CITY (id, country FK)
    ↑
    |
BILLIONARIES (id, city FK, personalInfo FK) ← PERSONAL_INFO (id)
    ↑
    |
WORKS (billionaire_id FK, company_id FK) → COMPANY (id)
```

### Table Details

#### ECONOMICS
- Economic indicators (CPI, GDP, tax rates)
- No dependencies

#### PERSONAL_INFO
- Personal biographical information
- No dependencies

#### COMPANY
- Company/organization data
- No dependencies

#### COUNTRY
- Country information with demographics
- **FK**: `economics` → ECONOMICS.id

#### CITY
- City information
- **FK**: `country` → COUNTRY.id

#### BILLIONARIES
- Main billionaire data
- **FK**: `city` → CITY.id
- **FK**: `personalInfo` → PERSONAL_INFO.id

#### WORKS
- Junction table for billionaire-company relationships
- **FK**: `billionaire_id` → BILLIONARIES.id
- **FK**: `company_id` → COMPANY.id

## Features

### NULL Checks
All scripts include NULL checks when looking up foreign keys. If a referenced record doesn't exist, the script will:
- Print a warning message
- Use NULL for the foreign key value (or skip the record)
- Continue execution without crashing

Example from `make_city.py`:
```python
cursor.execute('SELECT id FROM COUNTRY WHERE countryName = ?', (countryName,))
result = cursor.fetchone()

if result is None:
    print(f"⚠️  Warning: Country '{countryName}' not found, using NULL")
    country_id = None
else:
    country_id = result[0]
```

### Foreign Key Constraints
All foreign keys are explicitly defined with FOREIGN KEY clauses:
```sql
FOREIGN KEY (country) REFERENCES COUNTRY(id)
```

### Data Types
All tables use proper SQLite data types:
- `INTEGER` for IDs and integer values
- `TEXT` for strings
- `REAL` for floating-point numbers

## Troubleshooting

### Database Already Exists
The `create_b_db.py` script automatically removes any existing `b.db` file before creating a new one.

### Missing Foreign Key Reference
If you see warnings about missing foreign keys, ensure you're running the scripts in the correct order (use `create_b_db.py`).

### Foreign Keys Not Enforced
SQLite requires foreign key support to be explicitly enabled. The scripts automatically enable this:
```python
conn.execute("PRAGMA foreign_keys = ON;")
```

## Individual Script Usage

You can also run individual scripts for testing:

```bash
# Create just the ECONOMICS table
python make_economics.py

# Create just the COUNTRY table (requires ECONOMICS to exist)
python make_country.py
```

**Note**: When running individual scripts, you're responsible for ensuring dependencies are created first.

## Sample Data

Each script includes sample data for testing:
- 10 economic indicators
- 10 personal records
- 10 companies
- 10 countries
- 15 cities
- 10 billionaires
- 10 work relationships

## Security

The scripts follow security best practices:
- Use parameterized queries to prevent SQL injection
- Enable foreign key constraints
- Validate data before insertion
- Use proper transaction management (commit on success, rollback on error)
