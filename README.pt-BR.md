# appBilionarios - Aplicação de Banco de Dados de Bilionários

Uma aplicação web Flask completa para consultar e visualizar dados globais de bilionários.

## Características

- **Banco de Dados Completo**: Seis tabelas interconectadas com informações de bilionários
- **14 Consultas SQL**: Endpoints RESTful para consultas de dados e estatísticas
- **Interface Web Interativa**: Buscar, filtrar e explorar dados de bilionários
- **Painel de Estatísticas**: Visão geral da distribuição de riqueza global
- **Filtragem Multi-dimensional**: Por país, gênero, status selfmade e muito mais
- **Design Responsivo**: Funciona em desktop e dispositivos móveis
- **Interface em Português (Brasil)**: Toda a aplicação traduzida para PT-BR

## Estrutura do Banco de Dados

### Tabelas

1. **BILLIONAIRE**: Dados principais dos bilionários (rank, nome, patrimônio, empresa, cidade)
2. **PERSONAL**: Informações pessoais (idade, gênero, data de nascimento, cidadania)
3. **COMPANY**: Empresa/fonte da riqueza (organização, categoria, indústrias)
4. **CITY**: Informações da cidade (estado, região)
5. **COUNTRY**: Demografia do país (população, expectativa de vida, educação)
6. **COUNTRYECONOMY**: Indicadores econômicos (PIB, CPI, taxas de imposto)

### Relacionamentos
- BILLIONAIRE ←→ PERSONAL (1:1, via rank)
- BILLIONAIRE → COMPANY (N:1, via source)
- BILLIONAIRE → CITY (N:1, via cityName)
- PERSONAL → COUNTRY (N:1, via countryOfCitizenship)
- COUNTRY ←→ COUNTRYECONOMY (1:1, via countryName)

## As 14 Perguntas do Banco de Dados

### Seção: Perguntas BD (`/perguntas-bd`)

1. **Q1: Bilionários dos EUA** - Todos os bilionários dos Estados Unidos
2. **Q2: Top 10 por País** - Top 10 bilionários filtrados por país (disponível em `/top10`)
3. **Q3: Região Oeste dos EUA** - Bilionários da região oeste dos Estados Unidos
4. **Q4: Gênero Feminino** - Todas as bilionárias do gênero feminino
5. **Q5: Cidades com Mais Bilionários** - Cidade com maior número de bilionários
6. **Q6: Ordenar por Idade** - Bilionários ordenados por idade (disponível em `/all-list`)
7. **Q7: Idade > 50 e Rank ≥ 50** - Bilionários com mais de 50 anos e ranking ≥ 50
8. **Q8: Filtrar por Sobrenome** - Buscar bilionários por sobrenome (disponível em `/all-list`)
9. **Q9: Filtrar por Patrimônio** - Bilionários com patrimônio acima de X milhões (disponível em `/all-list`)
10. **Q10: Cidades por Patrimônio** - Cidades com maiores patrimônios totais
11. **Q11: Taxa de Imposto por País** - Relação entre taxa de imposto e bilionários por país
12. **Q12: Patrimônio vs PIB** - Comparação de patrimônio vs PIB (disponível em `/countries`)
13. **Q13: Expectativa de Vida** - Expectativa de vida restante por país (disponível em `/countries`)
14. **Q14: Selfmade vs Educação** - Relação entre bilionários selfmade e educação terciária

## Endpoints da Aplicação

### Endpoints Principais
- `GET /` - Página inicial com interface interativa
- `GET /top10` - Top 10 bilionários com filtros
- `GET /all-list` - Lista completa de bilionários
- `GET /countries` - Países com estatísticas de bilionários
- `GET /industries` - Indústrias com estatísticas de riqueza
- `GET /perguntas-bd` - Página com todas as 14 perguntas do banco de dados

### Endpoints de Perguntas
- `GET /perguntas-bd/q1` - Bilionários dos EUA
- `GET /perguntas-bd/q3` - Região oeste dos EUA
- `GET /perguntas-bd/q4` - Gênero feminino
- `GET /perguntas-bd/q5` - Cidades com mais bilionários
- `GET /perguntas-bd/q7` - Idade > 50 e rank ≥ 50
- `GET /perguntas-bd/q10` - Cidades por patrimônio
- `GET /perguntas-bd/q11` - Taxa de imposto por país
- `GET /perguntas-bd/q14` - Selfmade vs educação

### Endpoints de Filtros
- `GET /top10/q1/<país>` - Top 10 por país
- `GET /top10/q2/<indústria>` - Top 10 por indústria
- `GET /top10/q3/<idade>` - Top 10 por idade máxima
- `GET /all-list/q1/<ordem>` - Ordenar por idade (ASC/DESC)
- `GET /all-list/q2/<sobrenome>` - Filtrar por sobrenome
- `GET /all-list/q3/<patrimônio>` - Filtrar por patrimônio mínimo
- `GET /countries/q1/<país>` - Comparação patrimônio vs PIB
- `GET /countries/q2/<país>` - Bilionários nascidos no país
- `GET /countries/q3/<país>` - Expectativa de vida restante
- `GET /industries/q1/<indústria>` - Bilionários em indústria específica
- `GET /industries/q2/<quantidade>` - Indústrias com mais de X bilionários
- `GET /industries/q3/<ordem>` - Ordenar por patrimônio total

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Configuração

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/mtsguerra/appBilionarios.git
   cd appBilionarios
   ```

2. **Criar um ambiente virtual** (recomendado)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializar o banco de dados**
   ```bash
   python init_db.py
   ```
   Isso cria o `billionaires.db` com o schema e dados de exemplo.

5. **Executar a aplicação**
   ```bash
   python app.py
   ```
   A aplicação estará disponível em `http://localhost:5000`

## Uso

### Interface Web
1. Abra seu navegador em `http://localhost:5000`
2. Navegue pelas seções:
   - **Início**: Top 10 bilionários mais ricos
   - **Top 10**: Filtros por país, indústria e idade
   - **Lista Completa**: Todos os bilionários com opções de ordenação e filtro
   - **Países**: Estatísticas por país
   - **Indústrias**: Estatísticas por indústria
   - **Perguntas BD**: Todas as 14 consultas do banco de dados
3. Clique em qualquer nome para ver o perfil detalhado do bilionário
4. Use os formulários de busca para aplicar filtros personalizados

### Exemplos de Uso das Perguntas

**Ver todos os bilionários dos EUA:**
```
http://localhost:5000/perguntas-bd/q1
```

**Ver bilionários da região oeste dos EUA:**
```
http://localhost:5000/perguntas-bd/q3
```

**Ver relação entre selfmade e educação:**
```
http://localhost:5000/perguntas-bd/q14
```

## Estrutura do Projeto

```
appBilionarios/
├── app.py                          # Aplicação Flask principal
├── views.py                        # Rotas e lógica de visualização
├── init_db.py                      # Script de inicialização do banco
├── db.py                           # Funções auxiliares do banco
├── schema.sql                      # Definição do schema do banco
├── requirements.txt                # Dependências Python
├── billionaires.db                 # Banco de dados SQLite (criado após init)
├── templates/
│   ├── base.html                   # Template base
│   ├── erro.html                   # Página de erro
│   ├── navbar/
│   │   └── navbar.html             # Navegação
│   ├── home/
│   │   └── home.html               # Página inicial
│   ├── top10/
│   │   ├── top10.html              # Top 10 principal
│   │   ├── top10-queries.html      # Top 10 por país
│   │   ├── top10-industry.html     # Top 10 por indústria
│   │   └── top10-age.html          # Top 10 por idade
│   ├── all_list/
│   │   ├── all_list.html           # Lista completa
│   │   ├── all_list_asc_age.html   # Ordenado por idade
│   │   ├── all_list_by_last_name.html  # Filtrado por sobrenome
│   │   └── all_list_wealth.html    # Filtrado por patrimônio
│   ├── countries/
│   │   ├── countries.html          # Lista de países
│   │   ├── countries_wealth.html   # Comparação patrimônio vs PIB
│   │   ├── countries_born_amount.html  # Nascidos no país
│   │   └── countries_years_left.html   # Expectativa de vida
│   ├── industries/
│   │   ├── industries.html         # Lista de indústrias
│   │   ├── industries_specific_bil.html    # Bilionários em indústria
│   │   ├── industries_amount_of_bil.html   # Indústrias com X bilionários
│   │   └── industries_wealth.html          # Ordenado por patrimônio
│   ├── subject/
│   │   └── subject.html            # Perfil do bilionário
│   └── perguntas_bd/
│       ├── perguntas_bd.html       # Página principal das perguntas
│       ├── q1_bilionarios_eua.html # Q1: Bilionários dos EUA
│       ├── q3_regiao_oeste.html    # Q3: Região oeste
│       ├── q4_genero_feminino.html # Q4: Gênero feminino
│       ├── q5_cidade_mais_bilionarios.html # Q5: Cidades
│       ├── q7_mais_50_ranking.html # Q7: Idade > 50
│       ├── q10_cidades_patrimonio.html # Q10: Cidades patrimônio
│       ├── q11_tax_bilionarios.html    # Q11: Taxa imposto
│       └── q14_selfmade_education.html # Q14: Selfmade educação
├── static/
│   ├── base.css                    # Estilos base
│   ├── navbar.css                  # Estilos da navegação
│   ├── home.css                    # Estilos da home
│   ├── top10.css                   # Estilos do top10
│   ├── countries.css               # Estilos dos países
│   └── industries.css              # Estilos das indústrias
└── README.md                       # Este arquivo
```

## Desenvolvimento

### Adicionando Mais Dados
Para adicionar mais bilionários ou atualizar dados, modifique o script `init_db.py` e execute-o novamente:
```bash
python init_db.py
```

### Estendendo as Consultas
Para adicionar novas consultas:
1. Adicione uma nova rota em `views.py`
2. Crie o template correspondente em `templates/`
3. Opcionalmente, adicione um link na página de perguntas

Exemplo:
```python
@app.route('/perguntas-bd/q15')
def bd_q15_nova_consulta():
    """15. Descrição da nova consulta."""
    conn = get_db()
    query = '''
        -- Sua consulta SQL aqui
    '''
    cursor = conn.execute(query)
    results = cursor.fetchall()
    conn.close()
    return render_template('perguntas_bd/q15_nova_consulta.html', results=results)
```

## Tecnologias Utilizadas

- **Backend**: Flask 3.0.0, Python 3.x
- **Banco de Dados**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: CSS Grid, Flexbox, Gradientes
- **Segurança**: PRAGMA settings, prepared statements

## Dados de Exemplo

A aplicação inclui dados de exemplo para 8 bilionários de vários países e indústrias:
- Líderes de tecnologia (Jeff Bezos, Elon Musk, Bill Gates, Mark Zuckerberg)
- Bens de luxo (Bernard Arnault)
- Investimentos (Warren Buffett)
- Holdings diversificados (Mukesh Ambani, Carlos Slim Helu)

## Design Guidelines

### Esquema de Cores
- **Primário**: Gradiente roxo (#667eea → #764ba2)
- **Secundário**: Verde (#27ae60) para itens implementados
- **Terciário**: Azul (#3498db) para itens existentes
- **Neutro**: Branco (#ffffff) para cards e fundos

### Componentes
- Cards com sombra e bordas arredondadas
- Tabelas responsivas com efeito hover
- Botões com transição suave
- Layout limpo e organizado
- Emojis nos títulos para melhor visualização

## Segurança

A aplicação implementa várias medidas de segurança:
- **PRAGMA Settings**: `trusted_schema OFF`, `cell_size_check ON`, `foreign_keys ON`
- **Prepared Statements**: Todas as queries usam parâmetros preparados
- **Input Validation**: Validação de entrada em todas as rotas
- **Cache Control**: Headers para prevenir cache de dados sensíveis

## Licença

Este projeto é para fins educacionais.

## Autor

Criado como parte de um projeto de banco de dados e desenvolvimento web.

## Contribuindo

Contribuições são bem-vindas! Por favor:
1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## Suporte

Para questões ou suporte, abra uma issue no repositório GitHub.
