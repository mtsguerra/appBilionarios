"""Views for the Billionaires web application."""
import sqlite3
from contextlib import closing
from flask import render_template
from app import app


def get_db():
    """Create a database connection with security settings."""
    conn = sqlite3.connect('b.db')
    conn.row_factory = sqlite3.Row
    # Security settings
    conn.execute("PRAGMA trusted_schema = OFF;")
    conn.execute("PRAGMA cell_size_check = ON;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Home and Top 10 Routes
@app.route('/')
def home():
    """Home page with top 10 billionaires."""
    try:
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    b.rank, b.personName, b.finalWorth,
                    comp.source, pi.countryOfCitizenship
                FROM BILLIONARIES b
                LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
                LEFT JOIN WORKS w ON b.id = w.billionaire_id
                LEFT JOIN COMPANY comp ON w.company_id = comp.id
                ORDER BY b.rank
                LIMIT 10
            '''
            cursor = conn.execute(query)
            billionaires = cursor.fetchall()
        return render_template('home/home.html', billionaires=billionaires)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in home route: {e}')
        return render_template('erro.html', message='Database error occurred while loading the home page.')
    except Exception as e:
        app.logger.error(f'Unexpected error in home route: {e}')
        return render_template('erro.html', message='An unexpected error occurred while loading the home page.')


@app.route('/top10')
def top10():
    """Top 10 billionaires page."""
    try:
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    b.rank, b.personName, b.finalWorth,
                    comp.source, pi.countryOfCitizenship
                FROM BILLIONARIES b
                LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
                LEFT JOIN WORKS w ON b.id = w.billionaire_id
                LEFT JOIN COMPANY comp ON w.company_id = comp.id
                ORDER BY b.rank
                LIMIT 10
            '''
            cursor = conn.execute(query)
            billionaires = cursor.fetchall()
        return render_template('top10/top10.html', billionaires=billionaires)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in top10: {e}')
        return render_template('erro.html', message='Database error occurred.')
    except Exception as e:
        app.logger.error(f'Unexpected error in top10: {e}')
        return render_template('erro.html', message='An unexpected error occurred.')


@app.route('/top10/q1/<input>')
def top10_by_country(input):
    """Top 10 billionaires by country."""
    try:
        country = input.capitalize()
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    b.rank, b.personName, b.finalWorth,
                    comp.source, pi.countryOfCitizenship
                FROM BILLIONARIES b
                LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
                LEFT JOIN WORKS w ON b.id = w.billionaire_id
                LEFT JOIN COMPANY comp ON w.company_id = comp.id
                WHERE pi.countryOfCitizenship = ?
                ORDER BY b.rank
                LIMIT 10
            '''
            cursor = conn.execute(query, (country,))
            billionaires = cursor.fetchall()
        
        if not billionaires:
            return render_template('erro.html', message=f'No billionaires found for country: {country}')
        
        return render_template('top10/top10-queries.html', billionaires=billionaires, country=country)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in top10_by_country: {e}')
        return render_template('erro.html', message='Database error occurred.')
    except Exception as e:
        app.logger.error(f'Unexpected error in top10_by_country: {e}')
        return render_template('erro.html', message='An unexpected error occurred.')


@app.route('/top10/q2/<input>')
def top10_by_industry(input):
    """Top 10 billionaires by industry."""
    try:
        industry = input.capitalize()
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    b.rank, b.personName, b.finalWorth,
                    comp.source, pi.countryOfCitizenship, comp.category
                FROM BILLIONARIES b
                LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
                LEFT JOIN WORKS w ON b.id = w.billionaire_id
                LEFT JOIN COMPANY comp ON w.company_id = comp.id
                WHERE comp.category LIKE ?
                ORDER BY b.rank
                LIMIT 10
            '''
            cursor = conn.execute(query, (f'%{industry}%',))
            billionaires = cursor.fetchall()
        
        if not billionaires:
            return render_template('erro.html', message=f'No billionaires found for industry: {industry}')
        
        return render_template('top10/top10-industry.html', billionaires=billionaires, industry=industry)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in top10_by_industry: {e}')
        return render_template('erro.html', message='Database error occurred.')
    except Exception as e:
        app.logger.error(f'Unexpected error in top10_by_industry: {e}')
        return render_template('erro.html', message='An unexpected error occurred.')


@app.route('/top10/q3/<input>')
def top10_by_age(input):
    """Top 10 billionaires by age group."""
    try:
        age = int(input)
    except ValueError:
        return render_template('erro.html', message='Invalid age value. Please enter a valid integer.')
    
    try:
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    b.rank, b.personName, b.finalWorth,
                    comp.source, pi.countryOfCitizenship, pi.age
                FROM BILLIONARIES b
                LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
                LEFT JOIN WORKS w ON b.id = w.billionaire_id
                LEFT JOIN COMPANY comp ON w.company_id = comp.id
                WHERE pi.age <= ?
                ORDER BY b.rank
                LIMIT 10
            '''
            cursor = conn.execute(query, (age,))
            billionaires = cursor.fetchall()
        
        if not billionaires:
            return render_template('erro.html', message=f'No billionaires found under age: {age}')
        
        return render_template('top10/top10-age.html', billionaires=billionaires, age=age)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in top10_by_age: {e}')
        return render_template('erro.html', message='Database error occurred.')
    except Exception as e:
        app.logger.error(f'Unexpected error in top10_by_age: {e}')
        return render_template('erro.html', message='An unexpected error occurred.')


# Billionaire Profile Route
@app.route('/subject/<subject>')
def subject(subject):
    """Individual billionaire profile with navigation."""
    conn = get_db()
    
    # Get current billionaire
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, comp.source,
            c.cityName, pi.firstName, pi.lastName, pi.age, pi.gender, pi.birthDate,
            pi.countryOfCitizenship, comp.category, comp.industries
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN CITY c ON b.city = c.id
        LEFT JOIN WORKS w ON b.id = w.billionaire_id
        LEFT JOIN COMPANY comp ON w.company_id = comp.id
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
        FROM BILLIONARIES
        WHERE rank < ?
        ORDER BY rank DESC
        LIMIT 1
    '''
    cursor = conn.execute(prev_query, (billionaire['rank'],))
    prev_billionaire = cursor.fetchone()
    
    # Get next billionaire
    next_query = '''
        SELECT personName
        FROM BILLIONARIES
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
    try:
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    b.rank, b.personName, b.finalWorth,
                    comp.source, pi.countryOfCitizenship, pi.age
                FROM BILLIONARIES b
                LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
                LEFT JOIN WORKS w ON b.id = w.billionaire_id
                LEFT JOIN COMPANY comp ON w.company_id = comp.id
                ORDER BY b.rank
            '''
            cursor = conn.execute(query)
            billionaires = cursor.fetchall()
        return render_template('all_list/all_list.html', billionaires=billionaires)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in all_list: {e}')
        return render_template('erro.html', message='Database error occurred.')
    except Exception as e:
        app.logger.error(f'Unexpected error in all_list: {e}')
        return render_template('erro.html', message='An unexpected error occurred.')


@app.route('/all-list/q1/<input>')
def all_list_by_age(input):
    """List billionaires sorted by age."""
    # Validate sort direction using whitelist dictionary
    valid_orders = {'ASC': 'ASC', 'DESC': 'DESC', 'asc': 'ASC', 'desc': 'DESC'}
    order = valid_orders.get(input, 'ASC')  # Default to ASC if invalid input
    
    conn = get_db()
    # Build query safely using validated order value
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            comp.source, pi.countryOfCitizenship, pi.age
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN WORKS w ON b.id = w.billionaire_id
        LEFT JOIN COMPANY comp ON w.company_id = comp.id
        ORDER BY pi.age ''' + order
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
            b.rank, b.personName, b.finalWorth,
            comp.source, pi.countryOfCitizenship, pi.age, pi.lastName
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN WORKS w ON b.id = w.billionaire_id
        LEFT JOIN COMPANY comp ON w.company_id = comp.id
        WHERE pi.lastName LIKE ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (f'%{last_name}%',))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaire found with last name: {last_name}')
    
    return render_template('all_list/all_list_by_last_name.html', billionaires=billionaires, last_name=last_name)


@app.route('/all-list/q3/<input>')
def all_list_by_wealth(input):
    """Filter billionaires by minimum net worth."""
    try:
        min_wealth = float(input)
    except ValueError:
        return render_template('erro.html', message='Invalid wealth value. Please enter a valid number.')
    
    try:
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    b.rank, b.personName, b.finalWorth,
                    comp.source, pi.countryOfCitizenship, pi.age
                FROM BILLIONARIES b
                LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
                LEFT JOIN WORKS w ON b.id = w.billionaire_id
                LEFT JOIN COMPANY comp ON w.company_id = comp.id
                WHERE b.finalWorth >= ?
                ORDER BY b.finalWorth DESC
            '''
            cursor = conn.execute(query, (min_wealth,))
            billionaires = cursor.fetchall()
        
        if not billionaires:
            return render_template('erro.html', message=f'No billionaire found with net worth >= ${min_wealth}M')
        
        return render_template('all_list/all_list_wealth.html', billionaires=billionaires, min_wealth=min_wealth)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in all_list_by_wealth: {e}')
        return render_template('erro.html', message='Database error occurred.')
    except Exception as e:
        app.logger.error(f'Unexpected error in all_list_by_wealth: {e}')
        return render_template('erro.html', message='An unexpected error occurred.')


# Countries Routes
@app.route('/countries')
def countries():
    """List of countries with statistics."""
    conn = get_db()
    query = '''
        SELECT 
            pi.countryOfCitizenship as countryName,
            COUNT(*) as billionaireCount,
            SUM(b.finalWorth) as totalWorth,
            co.population, co.lifeExpectancy, e.gdp
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN COUNTRY co ON pi.countryOfCitizenship = co.countryName
        LEFT JOIN ECONOMICS e ON co.economics = e.id
        GROUP BY pi.countryOfCitizenship
        ORDER BY billionaireCount DESC
    '''
    cursor = conn.execute(query)
    countries = cursor.fetchall()
    conn.close()
    return render_template('countries/countries.html', countries=countries)


@app.route('/countries/q1/<input>')
def countries_wealth_comparison(input):
    """Compare billionaires' wealth with country's GDP per capita."""
    country = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            pi.countryOfCitizenship,
            co.population, e.gdp
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN COUNTRY co ON pi.countryOfCitizenship = co.countryName
        LEFT JOIN ECONOMICS e ON co.economics = e.id
        WHERE pi.countryOfCitizenship = ?
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
            pi.countryOfCitizenship, pi.age
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        WHERE pi.countryOfCitizenship = ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (country,))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaire found born in: {country}')
    
    return render_template('countries/countries_born_amount.html', billionaires=billionaires, country=country)


@app.route('/countries/q3/<input>')
def countries_life_expectancy(input):
    """Calculate remaining life expectancy for billionaires."""
    country = input.capitalize()
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, pi.age,
            pi.countryOfCitizenship,
            co.lifeExpectancy
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN COUNTRY co ON pi.countryOfCitizenship = co.countryName
        WHERE pi.countryOfCitizenship = ?
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
            comp.category,
            COUNT(DISTINCT b.id) as billionaireCount,
            SUM(b.finalWorth) as totalWorth
        FROM COMPANY comp
        LEFT JOIN WORKS w ON comp.id = w.company_id
        LEFT JOIN BILLIONARIES b ON w.billionaire_id = b.id
        GROUP BY comp.category
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
            b.rank, b.personName, b.finalWorth,
            comp.source, pi.countryOfCitizenship,
            comp.category, comp.industries
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN WORKS w ON b.id = w.billionaire_id
        LEFT JOIN COMPANY comp ON w.company_id = comp.id
        WHERE comp.category LIKE ?
        ORDER BY b.rank
    '''
    cursor = conn.execute(query, (f'%{industry}%',))
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message=f'No billionaire found in industry: {industry}')
    
    return render_template('industries/industries_specific_bil.html', billionaires=billionaires, industry=industry)


@app.route('/industries/q2/<input>')
def industries_amount(input):
    """Industries with more than X billionaires."""
    try:
        min_count = int(input)
    except ValueError:
        return render_template('erro.html', message='Invalid count value. Please enter a valid integer.')
    
    try:
        with closing(get_db()) as conn:
            query = '''
                SELECT 
                    comp.category,
                    COUNT(DISTINCT b.id) as billionaireCount
                FROM COMPANY comp
                LEFT JOIN WORKS w ON comp.id = w.company_id
                LEFT JOIN BILLIONARIES b ON w.billionaire_id = b.id
                GROUP BY comp.category
                HAVING COUNT(DISTINCT b.id) > ?
                ORDER BY billionaireCount DESC
            '''
            cursor = conn.execute(query, (min_count,))
            industries = cursor.fetchall()
        
        if not industries:
            return render_template('erro.html', message=f'No industry found with more than {min_count} billionaires')
        
        return render_template('industries/industries_amount_of_bil.html', industries=industries, min_count=min_count)
    except sqlite3.Error as e:
        app.logger.error(f'Database error in industries_amount: {e}')
        return render_template('erro.html', message='Database error occurred.')
    except Exception as e:
        app.logger.error(f'Unexpected error in industries_amount: {e}')
        return render_template('erro.html', message='An unexpected error occurred.')


@app.route('/industries/q3/<input>')
def industries_wealth(input):
    """Total net worth by industry sorted."""
    # Validate sort direction using whitelist dictionary
    valid_orders = {'ASC': 'ASC', 'DESC': 'DESC', 'asc': 'ASC', 'desc': 'DESC'}
    order = valid_orders.get(input, 'DESC')  # Default to DESC if invalid input
    
    conn = get_db()
    # Build query safely using validated order value
    query = '''
        SELECT 
            comp.category,
            COUNT(DISTINCT b.id) as billionaireCount,
            SUM(b.finalWorth) as totalWorth
        FROM COMPANY comp
        LEFT JOIN WORKS w ON comp.id = w.company_id
        LEFT JOIN BILLIONARIES b ON w.billionaire_id = b.id
        GROUP BY comp.category
        ORDER BY totalWorth ''' + order
    cursor = conn.execute(query)
    industries = cursor.fetchall()
    conn.close()
    
    return render_template('industries/industries_wealth.html', industries=industries, order=order)


# Database Questions Routes
@app.route('/perguntas-bd')
def perguntas_bd():
    """Page with all 14 database questions."""
    return render_template('perguntas_bd/perguntas_bd.html')


@app.route('/perguntas-bd/q1')
def bd_q1_bilionarios_eua():
    """1. All USA billionaires."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            comp.source, pi.countryOfCitizenship
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN WORKS w ON b.id = w.billionaire_id
        LEFT JOIN COMPANY comp ON w.company_id = comp.id
        WHERE pi.countryOfCitizenship = 'United States'
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='No billionaire found from USA')
    
    return render_template('perguntas_bd/q1_bilionarios_eua.html', billionaires=billionaires)


@app.route('/perguntas-bd/q3')
def bd_q3_regiao_oeste():
    """3. Billionaires from western USA region."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            c.cityName, pi.countryOfCitizenship,
            c.residenceStateRegion
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN CITY c ON b.city = c.id
        WHERE pi.countryOfCitizenship = 'United States'
        AND (c.residenceStateRegion LIKE '%West%' OR c.residenceStateRegion LIKE '%Northwest%')
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='No billionaire found in western USA region')
    
    return render_template('perguntas_bd/q3_regiao_oeste.html', billionaires=billionaires)


@app.route('/perguntas-bd/q4')
def bd_q4_genero_feminino():
    """4. Female billionaires."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            comp.source, pi.countryOfCitizenship, pi.gender, pi.age
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN WORKS w ON b.id = w.billionaire_id
        LEFT JOIN COMPANY comp ON w.company_id = comp.id
        WHERE pi.gender = 'F'
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='No female billionaire found')
    
    return render_template('perguntas_bd/q4_genero_feminino.html', billionaires=billionaires)


@app.route('/perguntas-bd/q5')
def bd_q5_cidade_mais_bilionarios():
    """5. City with highest number of billionaires."""
    conn = get_db()
    query = '''
        SELECT 
            c.cityName,
            c.state,
            c.residenceStateRegion,
            COUNT(*) as billionaireCount,
            SUM(b.finalWorth) as totalWorth
        FROM BILLIONARIES b
        LEFT JOIN CITY c ON b.city = c.id
        WHERE c.cityName IS NOT NULL
        GROUP BY c.cityName
        ORDER BY billionaireCount DESC, totalWorth DESC
        LIMIT 20
    '''
    cursor = conn.execute(query)
    cities = cursor.fetchall()
    conn.close()
    
    if not cities:
        return render_template('erro.html', message='Nenhuma cidade encontrada')
    
    return render_template('perguntas_bd/q5_cidade_mais_bilionarios.html', cities=cities)


@app.route('/perguntas-bd/q7')
def bd_q7_mais_50_anos_ranking():
    """7. Billionaires over 50 years old and rank equal to or greater than 50."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth,
            comp.source, pi.age, pi.countryOfCitizenship
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN WORKS w ON b.id = w.billionaire_id
        LEFT JOIN COMPANY comp ON w.company_id = comp.id
        WHERE pi.age > 50 AND b.rank >= 50
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='No billionaire found with these criteria')
    
    return render_template('perguntas_bd/q7_mais_50_ranking.html', billionaires=billionaires)


@app.route('/perguntas-bd/q10')
def bd_q10_cidades_maior_patrimonio():
    """10. Cities with the highest net worth among the billionaires living there."""
    conn = get_db()
    query = '''
        SELECT 
            c.cityName,
            c.state,
            c.residenceStateRegion,
            COUNT(*) as billionaireCount,
            SUM(b.finalWorth) as totalWorth,
            AVG(b.finalWorth) as avgWorth
        FROM BILLIONARIES b
        LEFT JOIN CITY c ON b.city = c.id
        WHERE c.cityName IS NOT NULL
        GROUP BY c.cityName
        ORDER BY totalWorth DESC
        LIMIT 20
    '''
    cursor = conn.execute(query)
    cities = cursor.fetchall()
    conn.close()
    
    if not cities:
        return render_template('erro.html', message='No city found')
    
    return render_template('perguntas_bd/q10_cidades_patrimonio.html', cities=cities)


@app.route('/perguntas-bd/q11')
def bd_q11_tax_bilionarios_pais():
    """11. Relationship between total tax and their respective numbers of billionaires by country."""
    conn = get_db()
    query = '''
        SELECT 
            pi.countryOfCitizenship as countryName,
            COUNT(*) as billionaireCount,
            e.totalTaxRate,
            SUM(b.finalWorth) as totalWorth,
            AVG(b.finalWorth) as avgWorth
        FROM BILLIONARIES b
        LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
        LEFT JOIN COUNTRY co ON pi.countryOfCitizenship = co.countryName
        LEFT JOIN ECONOMICS e ON co.economics = e.id
        WHERE e.totalTaxRate IS NOT NULL
        GROUP BY pi.countryOfCitizenship, e.totalTaxRate
        ORDER BY billionaireCount DESC
    '''
    cursor = conn.execute(query)
    countries = cursor.fetchall()
    conn.close()
    
    if not countries:
        return render_template('erro.html', message='Nenhum dado encontrado')
    
    return render_template('perguntas_bd/q11_tax_bilionarios.html', countries=countries)


@app.route('/perguntas-bd/q14')
def bd_q14_selfmade_education():
    """14. Relationship between selfmade billionaires and gross tertiary education."""
    conn = get_db()
    query = '''
        SELECT 
            co.countryName,
            co.grossTertiaryEducation,
            COUNT(CASE WHEN b.selfMade = 1 THEN 1 END) as selfMadeCount,
            COUNT(*) as totalBillionaires,
            ROUND(CAST(COUNT(CASE WHEN b.selfMade = 1 THEN 1 END) AS FLOAT) / COUNT(*) * 100, 2) as selfMadePercentage,
            AVG(b.finalWorth) as avgWorth
        FROM COUNTRY co
        LEFT JOIN PERSONAL_INFO pi ON co.countryName = pi.countryOfCitizenship
        LEFT JOIN BILLIONARIES b ON pi.id = b.personalInfo
        WHERE co.grossTertiaryEducation IS NOT NULL AND b.id IS NOT NULL
        GROUP BY co.countryName, co.grossTertiaryEducation
        HAVING totalBillionaires > 0
        ORDER BY co.grossTertiaryEducation DESC
    '''
    cursor = conn.execute(query)
    countries = cursor.fetchall()
    conn.close()
    
    if not countries:
        return render_template('erro.html', message='No data found')
    
    return render_template('perguntas_bd/q14_selfmade_education.html', countries=countries)
