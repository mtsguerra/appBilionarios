"""Database helper functions for the Billionaires application."""

# import sqlite3
# from flask import g

# DATABASE = 'b.db'

# def get_db():
#     """Get database connection."""
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row
#     return db

# def close_connection(exception):
#     """Close database connection."""
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# def query_db(query, args=(), one=False):
#     """Query the database."""
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv
