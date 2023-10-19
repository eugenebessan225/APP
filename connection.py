import os
import psycopg2
from flask import g


def get_conn():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'conn' not in g:
        g.conn = psycopg2.connect(
            host=os.getenv('HOST'),
            port=os.getenv("PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            connect_timeout=5
        )

    return g.conn


def close_db(e=None):
    """
    If this request connected to the database, close the
    connection.
    """
    conn = g.pop('conn', None)

    if conn is not None:
        conn.close()

    return None


def init_app(app):
    """
    Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
