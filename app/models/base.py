from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

db_config = {
    'host': '127.0.0.1',  
    'user': 'root',   
    'password': '58003695', 
    'database': 'ocean', 
    'port': 3306        
}

connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
                    
engine = create_engine(connection_string)
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False , autocommit = False , bind=engine)

