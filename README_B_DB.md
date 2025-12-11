# Usando o Banco de Dados b.db

Este documento explica como o aplicativo foi adaptado para funcionar com o banco de dados `b.db`.

## 📋 Sumário

1. [Visão Geral](#visão-geral)
2. [Estrutura do Banco b.db](#estrutura-do-banco-bdb)
3. [Diferenças em Relação ao Banco Anterior](#diferenças-em-relação-ao-banco-anterior)
4. [Arquivos de Suporte](#arquivos-de-suporte)
5. [Como Usar](#como-usar)
6. [Resolução de Problemas](#resolução-de-problemas)

## 🎯 Visão Geral

O aplicativo **appBilionarios** foi adaptado para funcionar com o banco de dados SQLite `b.db`, que possui uma estrutura normalizada com tabelas separadas para informações pessoais e econômicas.

### Principais Mudanças

- ✅ Banco de dados alterado de `billionaires.db` para `b.db`
- ✅ Tabela `PERSONAL_INFO` separada da tabela `BILLIONARIES`
- ✅ Tabela `ECONOMICS` separada da tabela `COUNTRY`
- ✅ Todas as queries SQL atualizadas com JOINs apropriados
- ✅ Mantida compatibilidade com todas as 28 rotas do aplicativo

## 🗄️ Estrutura do Banco b.db

O banco `b.db` possui 7 tabelas principais:

### 1. BILLIONARIES
Informações principais dos bilionários.

```sql
CREATE TABLE BILLIONARIES (
    id INTEGER PRIMARY KEY,
    rank INTEGER NOT NULL,
    finalWorth REAL NOT NULL,
    personName TEXT NOT NULL,
    selfMade INTEGER,
    status TEXT,
    city INTEGER,              -- FK → CITY.id
    personalInfo INTEGER       -- FK → PERSONAL_INFO.id
)
```

### 2. PERSONAL_INFO
Informações pessoais dos bilionários (idade, nome, nacionalidade, etc.).

```sql
CREATE TABLE PERSONAL_INFO (
    id INTEGER PRIMARY KEY,
    age INTEGER,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    birthDate TEXT,
    birthDay INTEGER,
    birthMonth INTEGER,
    birthYear INTEGER,
    gender TEXT,
    countryOfCitizenship TEXT
)
```

### 3. CITY
Informações sobre cidades.

```sql
CREATE TABLE CITY (
    id INTEGER PRIMARY KEY,
    cityName TEXT NOT NULL,
    state TEXT,
    residenceStateRegion TEXT,
    country INTEGER            -- FK → COUNTRY.id
)
```

### 4. COUNTRY
Informações sobre países.

```sql
CREATE TABLE COUNTRY (
    id INTEGER PRIMARY KEY,
    countryName TEXT,
    grossTertiaryEducation REAL,
    grossPrimaryEducation REAL,
    lifeExpectancy REAL,
    population INTEGER,
    latitude REAL,
    longitude REAL,
    economics INTEGER          -- FK → ECONOMICS.id
)
```

### 5. ECONOMICS
Dados econômicos dos países.

```sql
CREATE TABLE ECONOMICS (
    id INTEGER PRIMARY KEY,
    cpi REAL,
    cpiChange REAL,
    gdp REAL,
    taxRevenue REAL,
    totalTaxRate REAL
)
```

### 6. COMPANY
Informações sobre empresas e fontes de riqueza.

```sql
CREATE TABLE COMPANY (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    organization TEXT,
    category TEXT,
    industries TEXT
)
```

### 7. WORKS
Tabela de relacionamento entre bilionários e empresas (muitos-para-muitos).

```sql
CREATE TABLE WORKS (
    id INTEGER PRIMARY KEY,
    billionaire_id INTEGER,    -- FK → BILLIONARIES.id
    company_id INTEGER,        -- FK → COMPANY.id
    title TEXT
)
```

## 🔄 Diferenças em Relação ao Banco Anterior

### Banco Anterior (billionaires.db)

```
BILLIONARIES
├── rank, personName, finalWorth
├── age, firstName, lastName, gender  ← Dados pessoais DENTRO da tabela
└── countryOfCitizenship              ← Dados pessoais DENTRO da tabela

COUNTRY
├── countryName, population
└── gdp, totalTaxRate                 ← Dados econômicos DENTRO da tabela
```

### Banco Atual (b.db)

```
BILLIONARIES
├── rank, personName, finalWorth
├── personalInfo → PERSONAL_INFO      ← Dados pessoais em tabela SEPARADA
└── city → CITY → COUNTRY

PERSONAL_INFO
└── age, firstName, lastName, gender, countryOfCitizenship

COUNTRY
├── countryName, population
└── economics → ECONOMICS             ← Dados econômicos em tabela SEPARADA

ECONOMICS
└── gdp, totalTaxRate, cpi, cpiChange
```

### Exemplo de Query - Antes vs Depois

**ANTES (billionaires.db):**
```sql
SELECT b.personName, b.age, b.countryOfCitizenship
FROM BILLIONARIES b
WHERE b.age > 50
```

**DEPOIS (b.db):**
```sql
SELECT b.personName, pi.age, pi.countryOfCitizenship
FROM BILLIONARIES b
LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
WHERE pi.age > 50
```

## 📁 Arquivos de Suporte

O projeto inclui os seguintes arquivos para ajudar no uso do banco `b.db`:

### 1. `INSTRUCOES_IMPLEMENTACAO.txt`
Instruções detalhadas em português sobre:
- Como instalar o aplicativo
- Onde colocar o arquivo b.db
- Como executar e testar
- Troubleshooting completo

### 2. `create_sample_b_db.py`
Script Python para criar um banco `b.db` de exemplo com:
- Estrutura completa de todas as tabelas
- 10 bilionários de exemplo
- Dados de 5 países
- Relacionamentos configurados

**Como usar:**
```bash
python create_sample_b_db.py
```

### 3. `verificar_b_db.py`
Script de verificação que valida:
- Existência do arquivo b.db
- Presença de todas as tabelas
- Colunas necessárias em cada tabela
- Funcionamento dos JOINs
- Integridade dos dados

**Como usar:**
```bash
python verificar_b_db.py
```

## 🚀 Como Usar

### Passo 1: Preparar o Ambiente

```bash
# Clone o repositório
git clone https://github.com/mtsguerra/appBilionarios.git
cd appBilionarios

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### Passo 2: Configurar o Banco de Dados

Você tem duas opções:

**Opção A: Usar seu banco b.db existente**
```bash
# Copie seu arquivo b.db para a raiz do projeto
cp /caminho/para/seu/b.db .
```

**Opção B: Criar um banco de exemplo para testes**
```bash
# Execute o script de criação
python create_sample_b_db.py
```

### Passo 3: Verificar o Banco (Opcional mas Recomendado)

```bash
# Execute o script de verificação
python verificar_b_db.py
```

Se tudo estiver OK, você verá:
```
✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!
Seu banco b.db está pronto para uso com o aplicativo.
```

### Passo 4: Executar o Aplicativo

```bash
# Inicie o servidor Flask
python app.py
```

Acesse no navegador: `http://localhost:5000`

## 🔍 Resolução de Problemas

### Problema: "No such file or directory: b.db"

**Solução:**
- Verifique se o arquivo `b.db` está na raiz do projeto
- Execute `ls -la b.db` (Linux/Mac) ou `dir b.db` (Windows)
- Se não encontrado, copie o arquivo para o local correto

### Problema: "no such table: PERSONAL_INFO"

**Solução:**
- Seu banco não tem a estrutura correta
- Execute `python verificar_b_db.py` para verificar
- Se necessário, recrie o banco usando seus scripts Python originais

### Problema: Dados não aparecem no aplicativo

**Solução:**
- Execute `python verificar_b_db.py` para verificar os dados
- Certifique-se que a tabela BILLIONARIES tem registros
- Verifique se os relacionamentos (foreign keys) estão corretos

### Problema: Erros de JOIN nas queries

**Solução:**
- Execute `python verificar_b_db.py` para testar os JOINs
- Verifique se as tabelas PERSONAL_INFO e ECONOMICS existem
- Confirme que as foreign keys estão configuradas:
  - `BILLIONARIES.personalInfo` → `PERSONAL_INFO.id`
  - `COUNTRY.economics` → `ECONOMICS.id`

## 📊 Exemplo de Uso

### Verificar Estrutura do Banco

```bash
sqlite3 b.db ".schema BILLIONARIES"
```

### Contar Registros

```bash
sqlite3 b.db "SELECT COUNT(*) FROM BILLIONARIES;"
```

### Testar JOIN Manualmente

```sql
sqlite3 b.db
sqlite> SELECT 
    b.personName, 
    pi.age, 
    pi.countryOfCitizenship,
    comp.source
FROM BILLIONARIES b
LEFT JOIN PERSONAL_INFO pi ON b.personalInfo = pi.id
LEFT JOIN WORKS w ON b.id = w.billionaire_id
LEFT JOIN COMPANY comp ON w.company_id = comp.id
LIMIT 5;
```

## 📝 Notas Técnicas

### Foreign Keys Habilitadas

O aplicativo ativa foreign keys para garantir integridade:
```python
conn.execute("PRAGMA foreign_keys = ON;")
```

### Configurações de Segurança

```python
conn.execute("PRAGMA trusted_schema = OFF;")
conn.execute("PRAGMA cell_size_check = ON;")
```

### Row Factory

Usa `sqlite3.Row` para acesso por nome de coluna:
```python
conn.row_factory = sqlite3.Row
```

## 🤝 Contribuindo

Se encontrar problemas ou tiver sugestões:
1. Verifique a documentação em `INSTRUCOES_IMPLEMENTACAO.txt`
2. Execute `python verificar_b_db.py` para diagnóstico
3. Abra uma issue no GitHub com detalhes do problema

## 📚 Recursos Adicionais

- **README.md**: Documentação geral do projeto
- **INSTRUCOES_IMPLEMENTACAO.txt**: Guia completo de instalação
- **schema.sql**: Schema do banco anterior (referência)
- **recreate_database.sql**: Script do banco anterior (referência)

---

**Última atualização:** Dezembro 2024  
**Compatível com:** Python 3.8+, Flask 3.0.0, SQLite 3
