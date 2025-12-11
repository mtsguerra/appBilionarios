# appBilionarios - Billionaire Database Application

> 🇧🇷 [Versão em Português (Brasil)](README.pt-BR.md)

A complete Flask web application for querying and visualizing global billionaire data.

## Features

- **Comprehensive Database**: Six interconnected tables with billionaire information
- **14 SQL Queries**: RESTful endpoints for data queries and statistics
- **Interactive Web Interface**: Search, filter, and explore billionaire data
- **Statistics Dashboard**: Overview of global wealth distribution
- **Multi-dimensional Filtering**: By country, gender, self-made status, and more
- **Responsive Design**: Works on desktop and mobile devices
- **Portuguese Interface**: Full application translated to PT-BR

## Database Structure

### Tables

1. **BILLIONAIRE**: Core billionaire data (rank, name, worth, company, city)
2. **PERSONAL**: Personal information (age, gender, birthdate, citizenship)
3. **COMPANY**: Company/source of wealth (organization, category, industries)
4. **CITY**: City information (state, region)
5. **COUNTRY**: Country demographics (population, life expectancy, education)
6. **COUNTRYECONOMY**: Economic indicators (GDP, CPI, tax rates)

### Relationships
- BILLIONAIRE ←→ PERSONAL (1:1, via rank)
- BILLIONAIRE → COMPANY (N:1, via source)
- BILLIONAIRE → CITY (N:1, via cityName)
- PERSONAL → COUNTRY (N:1, via countryOfCitizenship)
- COUNTRY ←→ COUNTRYECONOMY (1:1, via countryName)

## The 14 Database Questions

### Database Questions Section (`/perguntas-bd`)

1. **Q1: USA Billionaires** - All billionaires from the United States
2. **Q2: Top 10 by Country** - Top 10 billionaires filtered by country (available at `/top10`)
3. **Q3: Western USA Region** - Billionaires from the western United States region
4. **Q4: Female Gender** - All female billionaires
5. **Q5: Cities with Most Billionaires** - City with the highest number of billionaires
6. **Q6: Sort by Age** - Billionaires sorted by age (available at `/all-list`)
7. **Q7: Age > 50 and Rank ≥ 50** - Billionaires over 50 years old and rank ≥ 50
8. **Q8: Filter by Last Name** - Search billionaires by last name (available at `/all-list`)
9. **Q9: Filter by Wealth** - Billionaires with wealth above X millions (available at `/all-list`)
10. **Q10: Cities by Wealth** - Cities with highest total wealth
11. **Q11: Tax Rate by Country** - Relationship between tax rate and billionaires by country
12. **Q12: Wealth vs GDP** - Comparison of wealth vs GDP (available at `/countries`)
13. **Q13: Life Expectancy** - Remaining life expectancy by country (available at `/countries`)
14. **Q14: Selfmade vs Education** - Relationship between selfmade billionaires and tertiary education

## Application Endpoints

### Main Endpoints
- `GET /` - Homepage with interactive UI
- `GET /top10` - Top 10 billionaires with filters
- `GET /all-list` - Complete list of billionaires
- `GET /countries` - Countries with billionaire statistics
- `GET /industries` - Industries with wealth statistics
- `GET /perguntas-bd` - Page with all 14 database questions

### Question Endpoints
- `GET /perguntas-bd/q1` - USA billionaires
- `GET /perguntas-bd/q3` - Western USA region
- `GET /perguntas-bd/q4` - Female gender
- `GET /perguntas-bd/q5` - Cities with most billionaires
- `GET /perguntas-bd/q7` - Age > 50 and rank ≥ 50
- `GET /perguntas-bd/q10` - Cities by wealth
- `GET /perguntas-bd/q11` - Tax rate by country
- `GET /perguntas-bd/q14` - Selfmade vs education

### Filter Endpoints
- `GET /top10/q1/<country>` - Top 10 by country
- `GET /top10/q2/<industry>` - Top 10 by industry
- `GET /top10/q3/<age>` - Top 10 by max age
- `GET /all-list/q1/<order>` - Sort by age (ASC/DESC)
- `GET /all-list/q2/<lastname>` - Filter by last name
- `GET /all-list/q3/<wealth>` - Filter by minimum wealth
- `GET /countries/q1/<country>` - Wealth vs GDP comparison
- `GET /countries/q2/<country>` - Billionaires born in country
- `GET /countries/q3/<country>` - Remaining life expectancy
- `GET /industries/q1/<industry>` - Billionaires in specific industry
- `GET /industries/q2/<count>` - Industries with more than X billionaires
- `GET /industries/q3/<order>` - Sort by total wealth

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/mtsguerra/appBilionarios.git
   cd appBilionarios
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```
   This creates `billionaires.db` with the schema and sample data.

5. **Run the application**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

## Usage

### Web Interface
1. Open your browser to `http://localhost:5000`
2. Navigate through sections:
   - **Home**: Top 10 richest billionaires
   - **Top 10**: Filters by country, industry, and age
   - **All List**: All billionaires with sorting and filtering options
   - **Countries**: Statistics by country
   - **Industries**: Statistics by industry
   - **Database Questions**: All 14 database queries
3. Click on any name to view detailed billionaire profile
4. Use search forms to apply custom filters

### Usage Examples

**View all USA billionaires:**
```
http://localhost:5000/perguntas-bd/q1
```

**View billionaires from western USA region:**
```
http://localhost:5000/perguntas-bd/q3
```

**View relationship between selfmade and education:**
```
http://localhost:5000/perguntas-bd/q14
```

## Project Structure

```
appBilionarios/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization script
├── schema.sql            # Database schema definition
├── requirements.txt      # Python dependencies
├── billionaires.db       # SQLite database (created after init)
├── templates/
│   └── index.html       # Main web interface
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── app.js       # Frontend JavaScript
└── README.md            # This file
```

## Development

### Adding More Data
To add more billionaires or update data, modify the `init_db.py` script and re-run it:
```bash
python init_db.py
```

### Extending the API
Add new endpoints in `app.py` following the existing pattern:
1. Define route with `@app.route()`
2. Create database connection
3. Execute SQL query
4. Return JSON response

## Technologies Used

- **Backend**: Flask 3.0.0, Python 3.x
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: RESTful JSON API

## Sample Data

The application includes sample data for 8 billionaires from various countries and industries, including:
- Technology leaders (Jeff Bezos, Elon Musk, Bill Gates, Mark Zuckerberg)
- Luxury goods (Bernard Arnault)
- Investment (Warren Buffett)
- Diversified holdings (Mukesh Ambani, Carlos Slim Helu)

## License

This project is for educational purposes.

## Author

Created as part of a database and web development project.