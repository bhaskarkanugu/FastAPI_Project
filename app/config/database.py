import os
import pyodbc
from fastapi import Depends

def get_connection():
    """
    Create a new pyodbc connection using the DB connection string
    from environment variables (retrieved from Conjur).
    """
    connection_string = os.getenv("CONJUR_DB_CONN_STRING")
    if not connection_string:
        raise ValueError("Database connection string not found in environment variables.")
    return pyodbc.connect(connection_string)

def get_db():
    """
    FastAPI dependency that yields a DB connection
    and ensures it is closed after use.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
