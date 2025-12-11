# appBilionarios - Billionaire Database Application

A complete Flask web application for querying and visualizing global billionaire data.

## Features

- **Comprehensive Database**: Six interconnected tables with billionaire information
- **RESTful API**: 11+ endpoints for data queries and statistics
- **Interactive Web Interface**: Search, filter, and explore billionaire data
- **Statistics Dashboard**: Overview of global wealth distribution
- **Multi-dimensional Filtering**: By country, gender, self-made status, and more
- **Responsive Design**: Works on desktop and mobile devices

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

## API Endpoints

### Core Endpoints
- `GET /` - Homepage with interactive UI
- `GET /api/billionaires` - List all billionaires with filters
  - Query params: `limit`, `offset`, `selfMade`, `minWorth`, `maxWorth`, `country`, `gender`
- `GET /api/billionaire/<rank>` - Get detailed billionaire information
- `GET /api/search?q=<query>` - Search billionaires by name

### Statistics Endpoints
- `GET /api/stats` - Overall statistics and distributions
- `GET /api/countries` - Countries with billionaire statistics
- `GET /api/cities` - Cities with billionaire counts
- `GET /api/industries` - Industries with wealth statistics
- `GET /api/companies` - Companies associated with billionaires
- `GET /api/age-distribution` - Age group distribution

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
2. Use the search bar to find specific billionaires
3. Apply filters to narrow down results
4. Click on any billionaire card to view detailed information
5. Explore statistics, countries, and industries sections

### API Usage Examples

**Get all billionaires:**
```bash
curl http://localhost:5000/api/billionaires
```

**Search for a billionaire:**
```bash
curl http://localhost:5000/api/search?q=Bezos
```

**Get billionaires by country:**
```bash
curl http://localhost:5000/api/billionaires?country=United%20States
```

**Get overall statistics:**
```bash
curl http://localhost:5000/api/stats
```

**Get specific billionaire details:**
```bash
curl http://localhost:5000/api/billionaire/1
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