"""Flask application for Billionaire database query and visualization."""
import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'billionaires.db'

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary."""
    return dict(zip(row.keys(), row))

@app.route('/')
def index():
    """Homepage."""
    return render_template('index.html')

@app.route('/api/billionaires')
def get_billionaires():
    """Get all billionaires with optional filters."""
    conn = get_db_connection()
    
    # Get query parameters for filtering
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', 0, type=int)
    self_made = request.args.get('selfMade', type=int)
    min_worth = request.args.get('minWorth', type=float)
    max_worth = request.args.get('maxWorth', type=float)
    country = request.args.get('country')
    gender = request.args.get('gender')
    
    # Build query
    query = '''
        SELECT 
            b.rank, b.personName, b.selfMade, b.status, b.cityName, 
            b.source, b.finalWorth, b.title,
            p.firstName, p.lastName, p.age, p.gender, p.countryOfCitizenship,
            c.organization, c.category, c.industries
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COMPANY c ON b.source = c.source
        WHERE 1=1
    '''
    params = []
    
    if self_made is not None:
        query += ' AND b.selfMade = ?'
        params.append(self_made)
    
    if min_worth is not None:
        query += ' AND b.finalWorth >= ?'
        params.append(min_worth)
    
    if max_worth is not None:
        query += ' AND b.finalWorth <= ?'
        params.append(max_worth)
    
    if country:
        query += ' AND p.countryOfCitizenship = ?'
        params.append(country)
    
    if gender:
        query += ' AND p.gender = ?'
        params.append(gender)
    
    query += ' ORDER BY b.rank'
    
    if limit:
        query += ' LIMIT ? OFFSET ?'
        params.extend([limit, offset])
    
    cursor = conn.execute(query, params)
    billionaires = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(billionaires)

@app.route('/api/billionaire/<int:rank>')
def get_billionaire(rank):
    """Get detailed information about a specific billionaire."""
    conn = get_db_connection()
    
    query = '''
        SELECT 
            b.rank, b.personName, b.selfMade, b.status, b.cityName, 
            b.source, b.finalWorth, b.title,
            p.firstName, p.lastName, p.birthDate, p.birthDay, p.birthMonth, 
            p.birthYear, p.age, p.gender, p.countryOfCitizenship,
            c.organization, c.category, c.industries,
            ct.state, ct.residenceStateRegion,
            co.lifeExpectancy, co.grossTertiaryEducation, co.grossPrimaryEducation,
            co.population, co.latitude, co.longitude,
            ce.cpi, ce.cpiChange, ce.taxRevenue, ce.totalTaxRate, ce.gdp
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COMPANY c ON b.source = c.source
        LEFT JOIN CITY ct ON b.cityName = ct.cityName
        LEFT JOIN COUNTRY co ON p.countryOfCitizenship = co.countryName
        LEFT JOIN COUNTRYECONOMY ce ON p.countryOfCitizenship = ce.countryName
        WHERE b.rank = ?
    '''
    
    cursor = conn.execute(query, (rank,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify(dict_from_row(row))
    else:
        return jsonify({'error': 'Billionaire not found'}), 404

@app.route('/api/search')
def search_billionaires():
    """Search billionaires by name."""
    query_param = request.args.get('q', '')
    
    if not query_param:
        return jsonify({'error': 'Search query parameter "q" is required'}), 400
    
    conn = get_db_connection()
    
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.title,
            p.age, p.gender, p.countryOfCitizenship,
            c.organization, c.category
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COMPANY c ON b.source = c.source
        WHERE b.personName LIKE ? OR p.firstName LIKE ? OR p.lastName LIKE ?
        ORDER BY b.rank
    '''
    
    search_term = f'%{query_param}%'
    cursor = conn.execute(query, (search_term, search_term, search_term))
    results = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(results)

@app.route('/api/countries')
def get_countries():
    """Get list of countries with billionaire counts and statistics."""
    conn = get_db_connection()
    
    query = '''
        SELECT 
            p.countryOfCitizenship as countryName,
            COUNT(*) as billionaireCount,
            AVG(b.finalWorth) as avgWorth,
            SUM(b.finalWorth) as totalWorth,
            co.population, co.lifeExpectancy,
            ce.gdp, ce.cpi
        FROM PERSONAL p
        JOIN BILLIONAIRE b ON p.rank = b.rank
        LEFT JOIN COUNTRY co ON p.countryOfCitizenship = co.countryName
        LEFT JOIN COUNTRYECONOMY ce ON p.countryOfCitizenship = ce.countryName
        GROUP BY p.countryOfCitizenship
        ORDER BY billionaireCount DESC
    '''
    
    cursor = conn.execute(query)
    countries = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(countries)

@app.route('/api/industries')
def get_industries():
    """Get list of industries with statistics."""
    conn = get_db_connection()
    
    query = '''
        SELECT 
            c.category,
            c.industries,
            COUNT(*) as billionaireCount,
            AVG(b.finalWorth) as avgWorth,
            SUM(b.finalWorth) as totalWorth
        FROM COMPANY c
        JOIN BILLIONAIRE b ON c.source = b.source
        GROUP BY c.category, c.industries
        ORDER BY billionaireCount DESC
    '''
    
    cursor = conn.execute(query)
    industries = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(industries)

@app.route('/api/stats')
def get_statistics():
    """Get overall statistics about billionaires."""
    conn = get_db_connection()
    
    # Overall statistics
    cursor = conn.execute('''
        SELECT 
            COUNT(*) as totalBillionaires,
            AVG(finalWorth) as avgWorth,
            MAX(finalWorth) as maxWorth,
            MIN(finalWorth) as minWorth,
            SUM(finalWorth) as totalWorth
        FROM BILLIONAIRE
    ''')
    overall_stats = dict_from_row(cursor.fetchone())
    
    # Gender distribution
    cursor = conn.execute('''
        SELECT gender, COUNT(*) as count
        FROM PERSONAL
        GROUP BY gender
    ''')
    gender_stats = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Self-made distribution
    cursor = conn.execute('''
        SELECT selfMade, COUNT(*) as count
        FROM BILLIONAIRE
        GROUP BY selfMade
    ''')
    selfmade_stats = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Age statistics
    cursor = conn.execute('''
        SELECT 
            AVG(age) as avgAge,
            MAX(age) as maxAge,
            MIN(age) as minAge
        FROM PERSONAL
    ''')
    age_stats = dict_from_row(cursor.fetchone())
    
    conn.close()
    
    return jsonify({
        'overall': overall_stats,
        'genderDistribution': gender_stats,
        'selfMadeDistribution': selfmade_stats,
        'ageStatistics': age_stats
    })

@app.route('/api/cities')
def get_cities():
    """Get list of cities with billionaire counts."""
    conn = get_db_connection()
    
    query = '''
        SELECT 
            b.cityName,
            ct.state,
            ct.residenceStateRegion,
            COUNT(*) as billionaireCount,
            AVG(b.finalWorth) as avgWorth
        FROM BILLIONAIRE b
        LEFT JOIN CITY ct ON b.cityName = ct.cityName
        GROUP BY b.cityName, ct.state, ct.residenceStateRegion
        ORDER BY billionaireCount DESC
    '''
    
    cursor = conn.execute(query)
    cities = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(cities)

@app.route('/api/age-distribution')
def get_age_distribution():
    """Get billionaire distribution by age groups."""
    conn = get_db_connection()
    
    query = '''
        SELECT 
            CASE 
                WHEN age < 30 THEN 'Under 30'
                WHEN age >= 30 AND age < 40 THEN '30-39'
                WHEN age >= 40 AND age < 50 THEN '40-49'
                WHEN age >= 50 AND age < 60 THEN '50-59'
                WHEN age >= 60 AND age < 70 THEN '60-69'
                WHEN age >= 70 AND age < 80 THEN '70-79'
                ELSE '80+'
            END as ageGroup,
            COUNT(*) as count,
            AVG(b.finalWorth) as avgWorth
        FROM PERSONAL p
        JOIN BILLIONAIRE b ON p.rank = b.rank
        GROUP BY ageGroup
        ORDER BY 
            CASE ageGroup
                WHEN 'Under 30' THEN 1
                WHEN '30-39' THEN 2
                WHEN '40-49' THEN 3
                WHEN '50-59' THEN 4
                WHEN '60-69' THEN 5
                WHEN '70-79' THEN 6
                ELSE 7
            END
    '''
    
    cursor = conn.execute(query)
    distribution = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(distribution)

@app.route('/api/companies')
def get_companies():
    """Get list of companies associated with billionaires."""
    conn = get_db_connection()
    
    query = '''
        SELECT 
            c.source,
            c.organization,
            c.category,
            c.industries,
            COUNT(b.rank) as billionaireCount,
            SUM(b.finalWorth) as totalWorth
        FROM COMPANY c
        LEFT JOIN BILLIONAIRE b ON c.source = b.source
        GROUP BY c.source, c.organization, c.category, c.industries
        ORDER BY billionaireCount DESC, totalWorth DESC
    '''
    
    cursor = conn.execute(query)
    companies = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(companies)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
