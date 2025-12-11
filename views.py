"""Views para a aplicação web de Bilionários."""
import sqlite3
from flask import render_template
from app import app


def get_db():
    """Cria uma conexão com o banco de dados com configurações de segurança."""
    conn = sqlite3.connect('billionaires.db')
    conn.row_factory = sqlite3.Row
    # Configurações de segurança
    conn.execute("PRAGMA trusted_schema = OFF;")
    conn.execute("PRAGMA cell_size_check = ON;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Rotas Home e Top 10
@app.route('/')
def home():
    """Página inicial com top 10 bilionários."""
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
    """Página de top 10 bilionários."""
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
    """Top 10 bilionários por país."""
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
    """Top 10 bilionários por indústria."""
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
    """Top 10 bilionários por faixa etária."""
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


# Rota de Perfil do Bilionário
@app.route('/subject/<subject>')
def subject(subject):
    """Perfil individual do bilionário com navegação."""
    conn = get_db()
    
    # Obter bilionário atual
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
        return render_template('erro.html', message=f'Bilionário não encontrado: {subject}')
    
    # Obter bilionário anterior
    prev_query = '''
        SELECT personName
        FROM BILLIONAIRE
        WHERE rank < ?
        ORDER BY rank DESC
        LIMIT 1
    '''
    cursor = conn.execute(prev_query, (billionaire['rank'],))
    prev_billionaire = cursor.fetchone()
    
    # Obter próximo bilionário
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


# Rotas de Lista Completa
@app.route('/all-list')
def all_list():
    """Lista completa de bilionários."""
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
    """Lista bilionários ordenados por idade."""
    # Validar e sanitizar direção da ordenação - apenas ASC ou DESC permitidos
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
    """Filtrar bilionários por sobrenome."""
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
        return render_template('erro.html', message=f'Nenhum bilionário encontrado com sobrenome: {last_name}')
    
    return render_template('all_list/all_list_by_last_name.html', billionaires=billionaires, last_name=last_name)


@app.route('/all-list/q3/<input>')
def all_list_by_wealth(input):
    """Filtrar bilionários por patrimônio mínimo."""
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
        return render_template('erro.html', message=f'Nenhum bilionário encontrado com patrimônio >= ${min_wealth}M')
    
    return render_template('all_list/all_list_wealth.html', billionaires=billionaires, min_wealth=min_wealth)


# Rotas de Países
@app.route('/countries')
def countries():
    """Lista de países com estatísticas."""
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
    """Comparar patrimônio dos bilionários com PIB per capita do país."""
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
    """Bilionários nascidos em um país específico."""
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
        return render_template('erro.html', message=f'Nenhum bilionário encontrado nascido em: {country}')
    
    return render_template('countries/countries_born_amount.html', billionaires=billionaires, country=country)


@app.route('/countries/q3/<input>')
def countries_life_expectancy(input):
    """Calcular expectativa de vida restante para bilionários."""
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


# Rotas de Indústrias
@app.route('/industries')
def industries():
    """Lista de indústrias com estatísticas."""
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
    """Bilionários em uma indústria específica."""
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
        return render_template('erro.html', message=f'Nenhum bilionário encontrado na indústria: {industry}')
    
    return render_template('industries/industries_specific_bil.html', billionaires=billionaires, industry=industry)


@app.route('/industries/q2/<input>')
def industries_amount(input):
    """Indústrias com mais de X bilionários."""
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
        return render_template('erro.html', message=f'Nenhuma indústria encontrada com mais de {min_count} bilionários')
    
    return render_template('industries/industries_amount_of_bil.html', industries=industries, min_count=min_count)


@app.route('/industries/q3/<input>')
def industries_wealth(input):
    """Patrimônio total por indústria ordenado."""
    # Validar e sanitizar direção da ordenação - apenas ASC ou DESC permitidos
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


# Rotas de Perguntas do Banco de Dados
@app.route('/perguntas-bd')
def perguntas_bd():
    """Página com todas as 14 perguntas do banco de dados."""
    return render_template('perguntas_bd/perguntas_bd.html')


@app.route('/perguntas-bd/q1')
def bd_q1_bilionarios_eua():
    """1. Todos bilionários dos EUA."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE p.countryOfCitizenship = 'United States'
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='Nenhum bilionário encontrado dos EUA')
    
    return render_template('perguntas_bd/q1_bilionarios_eua.html', billionaires=billionaires)


@app.route('/perguntas-bd/q3')
def bd_q3_regiao_oeste():
    """3. Bilionários da região oeste dos EUA."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.cityName,
            p.countryOfCitizenship,
            ci.residenceStateRegion
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        LEFT JOIN CITY ci ON b.cityName = ci.cityName
        WHERE p.countryOfCitizenship = 'United States'
        AND (ci.residenceStateRegion LIKE '%West%' OR ci.residenceStateRegion LIKE '%Northwest%')
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='Nenhum bilionário encontrado na região oeste dos EUA')
    
    return render_template('perguntas_bd/q3_regiao_oeste.html', billionaires=billionaires)


@app.route('/perguntas-bd/q4')
def bd_q4_genero_feminino():
    """4. Bilionários do gênero feminino."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.countryOfCitizenship, p.gender, p.age
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE p.gender = 'F'
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='Nenhuma bilionária do gênero feminino encontrada')
    
    return render_template('perguntas_bd/q4_genero_feminino.html', billionaires=billionaires)


@app.route('/perguntas-bd/q5')
def bd_q5_cidade_mais_bilionarios():
    """5. Cidade com maior número de bilionários."""
    conn = get_db()
    query = '''
        SELECT 
            b.cityName,
            ci.state,
            ci.residenceStateRegion,
            COUNT(*) as billionaireCount,
            SUM(b.finalWorth) as totalWorth
        FROM BILLIONAIRE b
        LEFT JOIN CITY ci ON b.cityName = ci.cityName
        WHERE b.cityName IS NOT NULL
        GROUP BY b.cityName
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
    """7. Bilionários com mais de 50 anos e ranking igual ou superior a 50."""
    conn = get_db()
    query = '''
        SELECT 
            b.rank, b.personName, b.finalWorth, b.source,
            p.age, p.countryOfCitizenship
        FROM BILLIONAIRE b
        LEFT JOIN PERSONAL p ON b.rank = p.rank
        WHERE p.age > 50 AND b.rank >= 50
        ORDER BY b.rank
    '''
    cursor = conn.execute(query)
    billionaires = cursor.fetchall()
    conn.close()
    
    if not billionaires:
        return render_template('erro.html', message='Nenhum bilionário encontrado com esses critérios')
    
    return render_template('perguntas_bd/q7_mais_50_ranking.html', billionaires=billionaires)


@app.route('/perguntas-bd/q10')
def bd_q10_cidades_maior_patrimonio():
    """10. Cidades com os maiores patrimônios entre os bilionários que vivem lá."""
    conn = get_db()
    query = '''
        SELECT 
            b.cityName,
            ci.state,
            ci.residenceStateRegion,
            COUNT(*) as billionaireCount,
            SUM(b.finalWorth) as totalWorth,
            AVG(b.finalWorth) as avgWorth
        FROM BILLIONAIRE b
        LEFT JOIN CITY ci ON b.cityName = ci.cityName
        WHERE b.cityName IS NOT NULL
        GROUP BY b.cityName
        ORDER BY totalWorth DESC
        LIMIT 20
    '''
    cursor = conn.execute(query)
    cities = cursor.fetchall()
    conn.close()
    
    if not cities:
        return render_template('erro.html', message='Nenhuma cidade encontrada')
    
    return render_template('perguntas_bd/q10_cidades_patrimonio.html', cities=cities)


@app.route('/perguntas-bd/q11')
def bd_q11_tax_bilionarios_pais():
    """11. Relação de total tax e seus respectivos números de bilionários por país."""
    conn = get_db()
    query = '''
        SELECT 
            p.countryOfCitizenship as countryName,
            COUNT(*) as billionaireCount,
            ce.totalTaxRate,
            SUM(b.finalWorth) as totalWorth,
            AVG(b.finalWorth) as avgWorth
        FROM PERSONAL p
        JOIN BILLIONAIRE b ON p.rank = b.rank
        LEFT JOIN COUNTRYECONOMY ce ON p.countryOfCitizenship = ce.countryName
        WHERE ce.totalTaxRate IS NOT NULL
        GROUP BY p.countryOfCitizenship, ce.totalTaxRate
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
    """14. Relação entre selfmade bilionários e gross tertiary education."""
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
        LEFT JOIN PERSONAL p ON co.countryName = p.countryOfCitizenship
        LEFT JOIN BILLIONAIRE b ON p.rank = b.rank
        WHERE co.grossTertiaryEducation IS NOT NULL AND b.rank IS NOT NULL
        GROUP BY co.countryName, co.grossTertiaryEducation
        HAVING totalBillionaires > 0
        ORDER BY co.grossTertiaryEducation DESC
    '''
    cursor = conn.execute(query)
    countries = cursor.fetchall()
    conn.close()
    
    if not countries:
        return render_template('erro.html', message='Nenhum dado encontrado')
    
    return render_template('perguntas_bd/q14_selfmade_education.html', countries=countries)
