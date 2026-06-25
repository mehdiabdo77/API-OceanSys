from app.core.base import engine, Base
from app.core.config import DB_DRIVER, DB_SERVER, DB_PORT, DB_DATABASE, DB_USER, DB_PASSWORD
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


def create_database_if_not_exists():
    # Connect to master database to create our database
    master_params = quote_plus(
        f"DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER},{DB_PORT};DATABASE=master;UID={DB_USER};PWD={DB_PASSWORD}"
    )
    master_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={master_params}")
    
    with master_engine.connect() as conn:
        # Enable autocommit for database creation
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        # Check if database exists
        result = conn.execute(text(f"SELECT name FROM sys.databases WHERE name = N'{DB_DATABASE}'"))
        if not result.fetchone():
            # Create database with Persian-friendly collation
            conn.execute(text(f"CREATE DATABASE [{DB_DATABASE}] COLLATE Persian_100_CI_AI"))
            print(f"Database '{DB_DATABASE}' created successfully with Persian collation!")
        else:
            print(f"Database '{DB_DATABASE}' already exists!")


def initialize_database():
    create_database_if_not_exists()
    Base.metadata.create_all(bind=engine)
