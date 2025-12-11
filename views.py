"""Views for the Billionaire web application."""
import sqlite3
from flask import render_template
from app import app


def get_db():
    """Create a database connection with security settings."""
    conn = sqlite3.connect('billionaires.db')
    conn.row_factory = sqlite3.Row
    # Security settings
    conn.execute("PRAGMA trusted_schema = OFF;")
    conn.execute("PRAGMA cell_size_check = ON;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Home and Top 10 Routes
@app.route('/')
def home():
    """Homepage with top 10 billionaires."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        ORDER BY b.rank
        LIMIT 10
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    return render_template('home/home.html', billionaires=billionaires)


@app.route('/top10')
def top10():
    """Top 10 billionaires page."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        ORDER BY b.rank
        LIMIT 10
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    return render_template('top10/top10.html', billionaires=billionaires)


@app.route('/top10/q1/<input>')
def top10_by_country(input):
    """Top 10 billionaires by country."""
    country = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE p.countryOfCitizenship = ?
        ORDER BY b.rank
        LIMIT 10
    '''
    cursor = conn.execute(query, (country,))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaires found for country: {country}')
    
    return render_template('top10/top10-queries.html', billionaires=billionaires, country=country)


@app.route('/top10/q2/<input>')
def top10_by_industry(input):
    """Top 10 billionaires by industry."""
    industry = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship, c.category
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COMPANY c ON b.source = c.source
        WHERE c.category LIKE ?
        ORDER BY b.rank
        LIMIT 10
    '''
    cursor = conn.execute(query, (f'%{industry}%',))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaires found for industry: {industry}')
    
    return render_template('top10/top10-industry.html', billionaires=billionaires, industry=industry)


@app.route('/top10/q3/<input>')
def top10_by_age(input):
    """Top 10 billionaires by age range."""
    age = input
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship, p.age
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE p.age <= ?
        ORDER BY b.rank
        LIMIT 10
    '''
    cursor = conn.execute(query, (age,))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaires found under age: {age}')
    
    return render_template('top10/top10-age.html', billionaires=billionaires, age=age)


# Subject Profile Route
@app.route('/subject/<subject>')
def subject(subject):
    """Individual billionaire profile with navigation."""
    conn = get_db()
    
    # Get current billionaire
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source, b.cityName,
            p.firstName, p.lastName, p.age, p.gender, p.birthDate,
            p.countryOfCitizenship,
            c.category, c.industries
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COMPANY c ON b.source = c.source
        WHERE b.personName = ?
    '''
    cursor = conn.execute(query, (subject,))
    billionaire = cursor.fetchone()
    
    if not billionaire:
        conn.close()
        return render_template('erro.html', message=f'Billionaire not found: {subject}')
    
    # Get previous billionaire
    prev_query = '''
        SELECT personName
        FROM BILLIONAIRE
        WHERE rank < ?
        ORDER BY rank DESC
        LIMIT 1
    '''
    cursor = conn.execute(prev_query, (billionaire['rank'],))
    prev_billionaire = cursor.fetchone()
    
    # Get next billionaire
    next_query = '''
        SELECT personName
        FROM BILLIONAIRE
        WHERE rank > ?
        ORDER BY rank ASC
        LIMIT 1
    '''
    cursor = conn.execute(next_query, (billionaire['rank'],))
    next_billionaire = cursor.fetchone()
    
    conn.close()
    
    return render_template('subject/subject.html', 
                         billionaire=billionaire,
                         prev=prev_billionaire['personName'] if prev_billionaire else None,
                         next=next_billionaire['personName'] if next_billionaire else None)


# All List Routes
@app.route('/all-list')
def all_list():
    """Complete list of billionaires."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship, p.age
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    return render_template('all_list/all_list.html', billionaires=billionaires)


@app.route('/all-list/q1/<input>')
def all_list_by_age(input):
    """List billionaires ordered by age."""
    # Validate and sanitize order direction - only allow ASC or DESC
    order = 'ASC' if input.upper() == 'ASC' else 'DESC'
    conn = get_db()
    # Safe to use order variable here as it's strictly validated above
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship, p.age
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        ORDER BY p.age ''' + order
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    return render_template('all_list/all_list_asc_age.html', billionaires=billionaires, order=order)


@app.route('/all-list/q2/<input>')
def all_list_by_last_name(input):
    """Filter billionaires by last name."""
    last_name = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship, p.age, p.lastName
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE p.lastName LIKE ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (f'%{last_name}%',))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaires found with last name: {last_name}')
    
    return render_template('all_list/all_list_by_last_name.html', billionaires=billionaires, last_name=last_name)


@app.route('/all-list/q3/<input>')
def all_list_by_wealth(input):
    """Filter billionaires by minimum wealth."""
    min_wealth = float(input)
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship, p.age
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE b.finalWorth >= ?
        ORDER BY b.finalWorth DESC
    '''
    cursor = conn.execute(query, (min_wealth,))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaires found with wealth >= ${min_wealth}M')
    
    return render_template('all_list/all_list_wealth.html', billionaires=billionaires, min_wealth=min_wealth)


# Countries Routes
@app.route('/countries')
def countries():
    """List of countries with statistics."""
    conn = get_db()
    query = '''
        SELECT 
            p.countryOfCitizenship as countryName,
            COUNT(*) as billionaireCount,
            SUM(b.finalWorth) as totalWorth,
            co.population, co.lifeExpectancy,
            ce.gdp
        FROM PERSONAL p
        JOIN BILLIONAIRE b ON p.rank = b.rank
        LEFT JOIN COUNTRY co ON p.countryOfCitizenship = co.countryName
        LEFT JOIN COUNTRYECONOMY ce ON p.countryOfCitizenship = ce.countryName
        GROUP BY p.countryOfCitizenship
        ORDER BY billionaireCount DESC
    '''
    cursor = conn.execute(query)
    countries = cursor.fetchall()
    conn.close()
    return render_template('countries/countries.html', countries=countries)


@app.route('/countries/q1/<input>')
def countries_wealth_comparison(input):
    """Compare billionaire wealth with country GDP per capita."""
    country = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            p.countryOfCitizenship,
            co.population, co.gdp,
            ce.gdp as gdp_value
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COUNTRY co ON p.countryOfCitizenship = co.countryName
        LEFT JOIN COUNTRYECONOMY ce ON p.countryOfCitizenship = ce.countryName
        WHERE p.countryOfCitizenship = ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (country,))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No data found for country: {country}')
    
    return render_template('countries/countries_wealth.html', billionaires=billionaires, country=country)


@app.route('/countries/q2/<input>')
def countries_born_in(input):
    """Billionaires born in a specific country."""
    country = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            p.countryOfCitizenship, p.age
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE p.countryOfCitizenship = ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (country,))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaires found born in: {country}')
    
    return render_template('countries/countries_born_amount.html', billionaires=billionaires, country=country)


@app.route('/countries/q3/<input>')
def countries_life_expectancy(input):
    """Calculate remaining life expectancy for billionaires."""
    country = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, p.age,
            p.countryOfCitizenship,
            co.lifeExpectancy
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COUNTRY co ON p.countryOfCitizenship = co.countryName
        WHERE p.countryOfCitizenship = ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (country,))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No data found for country: {country}')
    
    return render_template('countries/countries_years_left.html', billionaires=billionaires, country=country)


# Industries Routes
@app.route('/industries')
def industries():
    """List of industries with statistics."""
    conn = get_db()
    query = '''
        SELECT 
            c.category,
            COUNT(DISTINCT b.rank) as billionaireCount,
            SUM(b.finalWorth) as totalWorth
        FROM COMPANY c
        LEFT JOIN BILLIONAIRE b ON c.source = b.source
        GROUP BY c.category
        ORDER BY billionaireCount DESC
    '''
    cursor = conn.execute(query)
    industries = cursor.fetchall()
    conn.close()
    return render_template('industries/industries.html', industries=industries)


@app.route('/industries/q1/<input>')
def industries_specific_billionaires(input):
    """Billionaires in a specific industry."""
    industry = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship,
            c.category, c.industries
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN COMPANY c ON b.source = c.source
        WHERE c.category LIKE ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (f'%{industry}%',))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaires found in industry: {industry}')
    
    return render_template('industries/industries_specific_bil.html', billionaires=billionaires, industry=industry)


@app.route('/industries/q2/<input>')
def industries_amount(input):
    """Industries with more than X billionaires."""
    min_count = int(input)
    conn = get_db()
    query = '''
        SELECT 
            c.category,
            COUNT(DISTINCT b.rank) as billionaireCount
        FROM COMPANY c
        LEFT JOIN BILLIONAIRE b ON c.source = b.source
        GROUP BY c.category
        HAVING COUNT(DISTINCT b.rank) > ?
        ORDER BY billionaireCount DESC
    '''
    cursor = conn.execute(query, (min_count,))
    industries = cursor.fetchall()
    conn.close()
    
    if not industries:
        return render_template('erro.html', message=f'No industries found with more than {min_count} billionaires')
    
    return render_template('industries/industries_amount_of_bil.html', industries=industries, min_count=min_count)


@app.route('/industries/q3/<input>')
def industries_wealth(input):
    """Total wealth by industry ordered."""
    # Validate and sanitize order direction - only allow ASC or DESC
    order = 'ASC' if input.upper() == 'ASC' else 'DESC'
    conn = get_db()
    # Safe to use order variable here as it's strictly validated above
    query = '''
        SELECT 
            c.category,
            COUNT(DISTINCT b.rank) as billionaireCount,
            SUM(b.finalWorth) as totalWorth
        FROM COMPANY c
        LEFT JOIN BILLIONAIRE b ON c.source = b.source
        GROUP BY c.category
        ORDER BY totalWorth ''' + order
    cursor = conn.execute(query)
    industries = cursor.fetchall()
    conn.close()
    
    return render_template('industries/industries_wealth.html', industries=industries, order=order)
