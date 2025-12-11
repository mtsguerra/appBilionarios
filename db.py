"""Funções auxiliares de banco de dados para a aplicação de Bilionários."""

# import sqlite3
# from flask import g

# DATABASE = 'billionaires.db'

# def get_db():
#     """Obter conexão com banco de dados."""
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row
#     return db

# def close_connection(exception):
#     """Fechar conexão com banco de dados."""
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# def query_db(query, args=(), one=False):
#     """Consultar o banco de dados."""
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv
