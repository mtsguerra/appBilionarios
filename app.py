import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask, request
import logging
import db

APP = Flask(__name__)

# Página Inicial com Menu
@APP.route('/')
def index():
    return render_template('index.html')

# 1. Todos bilionários dos EUA
@APP.route('/q1')
def q1():
    # Buscando pela cidadania na tabela PERSONAL_INFO
    sql = """
          SELECT b.rank, b.personName, b.finalWorth, p.countryOfCitizenship
          FROM BILLIONARIES b
                   JOIN PERSONAL_INFO p ON b.personalInfo = p.id
          WHERE p.countryOfCitizenship = 'United States'
          ORDER BY b.rank ASC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Bilionários dos EUA', rows=results, headers=['Ranking', 'Nome', 'Patrimônio', 'País'])

# 2. Número de bilionários com patrimônio maior que X
@APP.route('/q2')
def q2():
    x_value = request.args.get('x', 1000) # Default 1000 se não informado
    sql = "SELECT count(*) as total FROM BILLIONARIES WHERE finalWorth > ?"
    result = db.execute(sql, [x_value]).fetchone()
    return render_template('result_single.html', title=f'Bilionários com patrimônio > {x_value}', value=result['total'], label='Quantidade')

# 3. Bilionários da região oeste dos EUA
@APP.route('/q3')
def q3():
    sql = """
          SELECT b.personName, c.cityName, c.residenceStateRegion
          FROM BILLIONARIES b
                   JOIN CITY c ON b.city = c.id
                   JOIN COUNTRY co ON c.country = co.id
          WHERE c.residenceStateRegion = 'West' AND co.countryName = 'United States' \
          """
    # Nota: countryName pode estar armazenado como Texto ou ID dependendo da normalização exata,
    # ajustado aqui assumindo texto ou usando PERSONAL_INFO se falhar.
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Bilionários do Oeste dos EUA', rows=results, headers=['Nome', 'Cidade', 'Região'])

# 4. Bilionários do gênero feminino
@APP.route('/q4')
def q4():
    sql = """
          SELECT b.personName, b.finalWorth, p.gender
          FROM BILLIONARIES b
                   JOIN PERSONAL_INFO p ON b.personalInfo = p.id
          WHERE p.gender = 'F' \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Bilionários Mulheres', rows=results, headers=['Nome', 'Patrimônio', 'Gênero'])

# 5. Cidade com maior número de bilionários
@APP.route('/q5')
def q5():
    sql = """
          SELECT c.cityName, count(b.id) as qtd
          FROM BILLIONARIES b
                   JOIN CITY c ON b.city = c.id
          GROUP BY c.cityName
          ORDER BY qtd DESC
              LIMIT 1 \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Cidade com mais Bilionários', rows=results, headers=['Cidade', 'Quantidade'])

# 6. Bilionários com menos de 50 anos
@APP.route('/q6')
def q6():
    sql = """
          SELECT b.personName, p.age, b.finalWorth
          FROM BILLIONARIES b
                   JOIN PERSONAL_INFO p ON b.personalInfo = p.id
          WHERE p.age < 50 AND p.age IS NOT NULL
          ORDER BY p.age ASC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Bilionários com menos de 50 anos', rows=results, headers=['Nome', 'Idade', 'Patrimônio'])

# 7. Bilionários com mais de 50 anos e ranking igual ou superior a 50 (Top 50)
@APP.route('/q7')
def q7():
    sql = """
          SELECT b.rank, b.personName, p.age
          FROM BILLIONARIES b
                   JOIN PERSONAL_INFO p ON b.personalInfo = p.id
          WHERE p.age > 50 AND b.rank <= 50
          ORDER BY b.rank ASC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Top 50 Bilionários (+50 anos)', rows=results, headers=['Rank', 'Nome', 'Idade'])

# 8. Média de patrimônio por país
@APP.route('/q8')
def q8():
    # Usando countryOfCitizenship de Personal Info para agrupar
    sql = """
          SELECT p.countryOfCitizenship, AVG(b.finalWorth) as media_patrimonio
          FROM BILLIONARIES b
                   JOIN PERSONAL_INFO p ON b.personalInfo = p.id
          GROUP BY p.countryOfCitizenship
          ORDER BY media_patrimonio DESC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Média de Patrimônio por País', rows=results, headers=['País', 'Média de Patrimônio'])

# 9. Indústrias e suas respectivas contagem de bilionários
@APP.route('/q9')
def q9():
    sql = """
          SELECT cp.industries, count(DISTINCT w.billionaire_id) as qtd
          FROM WORKS w
                   JOIN COMPANY cp ON w.company_id = cp.id
          GROUP BY cp.industries
          ORDER BY qtd DESC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Bilionários por Indústria', rows=results, headers=['Indústria', 'Quantidade'])

# 10. Cidades com os maiores patrimônios (Soma)
@APP.route('/q10')
def q10():
    sql = """
          SELECT c.cityName, SUM(b.finalWorth) as total_wealth
          FROM BILLIONARIES b
                   JOIN CITY c ON b.city = c.id
          GROUP BY c.cityName
          ORDER BY total_wealth DESC
              LIMIT 20 \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Cidades com Maior Patrimônio Acumulado', rows=results, headers=['Cidade', 'Patrimônio Total'])

# 11. Relação de total tax e seus respectivos números de bilionários por país
@APP.route('/q11')
def q11():
    # Join complexo para chegar em Economics
    sql = """
          SELECT co.countryName, e.totalTaxRate, count(b.id) as num_bilionarios
          FROM BILLIONARIES b
                   JOIN CITY c ON b.city = c.id
                   JOIN COUNTRY co ON c.country = co.id
                   JOIN ECONOMICS e ON co.economics = e.id
          GROUP BY co.countryName
          ORDER BY e.totalTaxRate DESC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Taxa de Imposto vs Nº Bilionários', rows=results, headers=['País', 'Total Tax Rate', 'Qtd Bilionários'])

# 12. Quantidade de bilionários por categorias e seus patrimônios acumulados
@APP.route('/q12')
def q12():
    sql = """
          SELECT cp.category, count(DISTINCT b.id) as qtd, SUM(b.finalWorth) as total
          FROM BILLIONARIES b
                   JOIN WORKS w ON b.id = w.billionaire_id
                   JOIN COMPANY cp ON w.company_id = cp.id
          GROUP BY cp.category
          ORDER BY total DESC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Categorias: Qtd e Patrimônio', rows=results, headers=['Categoria', 'Quantidade', 'Patrimônio Total'])

# 13. Relação entre o GDP e a média de patrimônio por países
@APP.route('/q13')
def q13():
    sql = """
          SELECT co.countryName, e.gdp, AVG(b.finalWorth) as avg_wealth
          FROM BILLIONARIES b
                   JOIN CITY c ON b.city = c.id
                   JOIN COUNTRY co ON c.country = co.id
                   JOIN ECONOMICS e ON co.economics = e.id
          GROUP BY co.countryName \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='GDP vs Média de Patrimônio', rows=results, headers=['País', 'GDP', 'Média Patrimônio'])

# 14. Relação entre selfmade bilionários e gross tertiary education
@APP.route('/q14')
def q14():
    # Agrupando por país para ver a taxa de educação vs quantos são self-made
    sql = """
          SELECT co.countryName, co.grossTertiaryEducation,
                 SUM(CASE WHEN b.selfMade = 1 THEN 1 ELSE 0 END) as self_made_count,
                 COUNT(b.id) as total_billionaires
          FROM BILLIONARIES b
                   JOIN CITY c ON b.city = c.id
                   JOIN COUNTRY co ON c.country = co.id
          GROUP BY co.countryName
          ORDER BY self_made_count DESC \
          """
    results = db.execute(sql).fetchall()
    return render_template('result_list.html', title='Self-Made vs Educação Terciária', rows=results, headers=['País', 'Educação Terciária (%)', 'Qtd Self-Made', 'Total Bilionários'])