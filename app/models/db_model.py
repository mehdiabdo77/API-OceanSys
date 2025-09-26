from sqlalchemy import create_engine

db_config = {
    'host': '127.0.0.1',  
    'user': 'root',   
    'password': '58003695', 
    'database': 'ocean', 
    'port': 3306        
}

connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
engine = create_engine(connection_string)
