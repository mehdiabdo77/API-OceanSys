from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
from urllib.parse import quote_plus
from app.core.config import DB_DRIVER, DB_SERVER, DB_PORT, DB_DATABASE, DB_USER, DB_PASSWORD

params = quote_plus(f"DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER},{DB_PORT};DATABASE={DB_DATABASE};UID={DB_USER};PWD={DB_PASSWORD}")
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
                    
engine = create_engine(connection_string)
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False , autocommit = False , bind=engine)

