from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 9000))

DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_SERVER = os.getenv("DB_SERVER", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_DATABASE = os.getenv("DB_DATABASE", "ocean")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD")

