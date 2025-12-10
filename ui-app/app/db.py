import psycopg
from flask import current_app, g

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = psycopg.connect(current_app.config['DATABASE_URL'])
    return g.db

def close_db(e=None):
    """
    Closes the database connection.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
