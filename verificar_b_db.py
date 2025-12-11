"""
Script para verificar a estrutura e integridade do banco b.db.
Execute este script para validar se o seu banco b.db está correto.
"""
import sqlite3
import os
import sys

def verificar_b_db():
    """Verifica se o banco b.db existe e tem a estrutura correta."""
    
    print("="*70)
    print("VERIFICAÇÃO DO BANCO DE DADOS b.db")
    print("="*70)
    print()
    
    # Verifica se o arquivo existe
    if not os.path.exists('b.db'):
        print("❌ ERRO: Arquivo b.db não encontrado!")
        print("\nO arquivo b.db deve estar na mesma pasta deste script.")
        print("Verifique as instruções em INSTRUCOES_IMPLEMENTACAO.txt")
        return False
    
    print("✓ Arquivo b.db encontrado")
    
    # Conecta ao banco
    try:
        conn = sqlite3.connect('b.db')
        cursor = conn.cursor()
        print("✓ Conexão com banco estabelecida")
    except Exception as e:
        print(f"❌ ERRO ao conectar: {e}")
        return False
    
    # Tabelas esperadas
    expected_tables = [
        'BILLIONARIES',
        'PERSONAL_INFO',
        'CITY',
        'COUNTRY',
        'ECONOMICS',
        'COMPANY',
        'WORKS'
    ]
    
    print("\n" + "-"*70)
    print("VERIFICANDO TABELAS")
    print("-"*70)
    
    # Verifica tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    all_tables_ok = True
    for table in expected_tables:
        if table in existing_tables:
            print(f"✓ Tabela {table} existe")
        else:
            print(f"❌ Tabela {table} NÃO ENCONTRADA")
            all_tables_ok = False
    
    if not all_tables_ok:
        print("\n❌ Banco não tem todas as tabelas necessárias!")
        conn.close()
        return False
    
    print("\n" + "-"*70)
    print("VERIFICANDO COLUNAS")
    print("-"*70)
    
    # Verifica colunas importantes
    checks = [
        ("BILLIONARIES", ["id", "rank", "finalWorth", "personName", "personalInfo", "city"]),
        ("PERSONAL_INFO", ["id", "age", "firstName", "lastName", "countryOfCitizenship"]),
        ("CITY", ["id", "cityName", "country"]),
        ("COUNTRY", ["id", "countryName", "economics"]),
        ("ECONOMICS", ["id", "gdp", "totalTaxRate"]),
        ("COMPANY", ["id", "source", "category"]),
        ("WORKS", ["id", "billionaire_id", "company_id"])
    ]
    
    all_columns_ok = True
    for table, expected_cols in checks:
        cursor.execute(f"PRAGMA table_info({table});")
        existing_cols = [row[1] for row in cursor.fetchall()]
        
        missing_cols = [col for col in expected_cols if col not in existing_cols]
        
        if missing_cols:
            print(f"❌ Tabela {table} faltando colunas: {', '.join(missing_cols)}")
            all_columns_ok = False
        else:
            print(f"✓ Tabela {table} tem todas as colunas necessárias")
    
    if not all_columns_ok:
        print("\n❌ Banco não tem todas as colunas necessárias!")
        conn.close()
        return False
    
    print("\n" + "-"*70)
    print("VERIFICANDO DADOS")
    print("-"*70)
    
    # Conta registros
    tables_with_data = []
    for table in expected_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        tables_with_data.append((table, count))
        
        if count > 0:
            print(f"✓ {table}: {count} registros")
        else:
            print(f"⚠️  {table}: 0 registros (vazio)")
    
    # Verifica se BILLIONARIES tem dados
    billionaries_count = next(count for table, count in tables_with_data if table == 'BILLIONARIES')
    if billionaries_count == 0:
        print("\n⚠️  AVISO: Tabela BILLIONARIES está vazia!")
        print("O aplicativo não mostrará dados sem bilionários cadastrados.")
    
    print("\n" + "-"*70)
    print("TESTANDO JOINS")
    print("-"*70)
    
    # Testa JOINs principais
    try:
        # JOIN com PERSONAL_INFO
        cursor.execute('''
            SELECT b.personName, pi.age, pi.countryOfCitizenship
            FROM BILLIONARIES b
            LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
            LIMIT 1
        ''')
        result = cursor.fetchone()
        if result:
            print(f"✓ JOIN BILLIONARIES ↔ PERSONAL_INFO funcionando")
            print(f"  Exemplo: {result[0]}, {result[1]} anos, {result[2]}")
        else:
            print("⚠️  JOIN BILLIONARIES ↔ PERSONAL_INFO retornou vazio")
        
        # JOIN com CITY e COUNTRY
        cursor.execute('''
            SELECT b.personName, c.cityName, co.countryName
            FROM BILLIONARIES b
            LEFT JOIN CITY c ON b.city = c.id
            LEFT JOIN COUNTRY co ON c.country = co.id
            LIMIT 1
        ''')
        result = cursor.fetchone()
        if result:
            print(f"✓ JOIN BILLIONARIES ↔ CITY ↔ COUNTRY funcionando")
            print(f"  Exemplo: {result[0]} mora em {result[1]}, {result[2]}")
        else:
            print("⚠️  JOIN BILLIONARIES ↔ CITY ↔ COUNTRY retornou vazio")
        
        # JOIN com ECONOMICS
        cursor.execute('''
            SELECT co.countryName, e.gdp, e.totalTaxRate
            FROM COUNTRY co
            LEFT JOIN ECONOMICS e ON co.economics = e.id
            LIMIT 1
        ''')
        result = cursor.fetchone()
        if result:
            print(f"✓ JOIN COUNTRY ↔ ECONOMICS funcionando")
            if result[1] and result[2]:
                print(f"  Exemplo: {result[0]}, PIB: {result[1]}, Taxa: {result[2]}%")
        else:
            print("⚠️  JOIN COUNTRY ↔ ECONOMICS retornou vazio")
        
        # JOIN com WORKS e COMPANY
        cursor.execute('''
            SELECT b.personName, comp.source, w.title
            FROM BILLIONARIES b
            LEFT JOIN WORKS w ON b.id = w.billionaire_id
            LEFT JOIN COMPANY comp ON w.company_id = comp.id
            LIMIT 1
        ''')
        result = cursor.fetchone()
        if result:
            print(f"✓ JOIN BILLIONARIES ↔ WORKS ↔ COMPANY funcionando")
            print(f"  Exemplo: {result[0]} - {result[1]} ({result[2]})")
        else:
            print("⚠️  JOIN BILLIONARIES ↔ WORKS ↔ COMPANY retornou vazio")
        
    except Exception as e:
        print(f"❌ ERRO ao testar JOINs: {e}")
        conn.close()
        return False
    
    conn.close()
    
    print("\n" + "="*70)
    print("✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70)
    print("\nSeu banco b.db está pronto para uso com o aplicativo.")
    print("Execute: python app.py")
    print()
    
    return True

if __name__ == '__main__':
    sucesso = verificar_b_db()
    sys.exit(0 if sucesso else 1)
