import os
import pymssql 
from fastapi import Depends

def get_connection():
    """
    Create a new pymssql connection using the DB connection string
    from environment variables (retrieved from Conjur).
    """
    # Note: pymssql's connect method takes separate arguments, not a single connection string.
    # We'll need to parse the string or get separate environment variables.
    # Assuming the environment variable CONJUR_DB_CONN_STRING holds a string like:
    # "server=your_server;database=your_db;user=your_user;password=your_password"
    # We will need to retrieve the individual parts.
    
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([server, database, user, password]):
        raise ValueError("One or more database connection details not found in environment variables.")

    # The pymssql.connect method requires separate arguments for each credential
    return pymssql.connect(
        server=server,
        user=user,
        password=password,
        database=database,
        as_dict=True # This returns query results as dictionaries, which is often more convenient
    )

def get_db():
    """
    FastAPI dependency that yields a DB connection
    and ensures it is closed after use.
    """
    conn = get_connection()
    try:
        # yield the connection for the request handler to use
        yield conn
    finally:
        # ensure the connection is closed when the request is complete
        conn.close()
