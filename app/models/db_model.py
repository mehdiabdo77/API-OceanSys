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

connection_string = f"mysql+pymysql://{db_config['user']}:{db_config
                    ['password']}@{db_config['host']}:{db_config
                    ['port']}/{db_config['database']}"
                    
engine = create_engine(connection_string)
base = declarative_base()
SessionLocal = sessionmaker(autoflush=False , autocommit = False , bind=engine)

# TODO اسم ستون ها دیتا بیس از فارسی به اینگلیسی تغییر بده تو اینده
class Customer(base):
    __tablename__ = "customer"
    
    کد_مشتری = Column(Integer, primary_key=True)
    نام_مشتری = Column(String(255), nullable=True)
    تابلو_مشستری = Column(String(255), nullable=True)
    کد_ملی = Column(String(20), nullable=True)
    محدوده = Column(String(100), nullable=True)
    ناحیه = Column(String(100), nullable=True)
    مسیر = Column(String(100), nullable=True)
    Latitude = Column(DECIMAL(9, 6), nullable=True)
    Longitude = Column(DECIMAL(9, 6), nullable=True)
    وضعیت = Column(String(50), nullable=True)
    آدرس_مشتری = Column(Text, nullable=True)
    تلفن_اول = Column(String(20), nullable=True)
    تلفن_همراه = Column(String(20), nullable=True)
    کد_پستی_مشتری = Column(String(20), nullable=True)

class User(Base):
    __tablename__ = "user_tbl"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    department_id = Column(Integer, ForeignKey("department_tbl.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("position_tbl.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at_jalali = Column(String(10), nullable=False)
    updated_at_jalali = Column(String(10), nullable=False)
    
    visit_reports = relationship("VisitReport", back_populates="user")
    

class VisitReport(Base):
    __tablename__ = "visit_reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.کد_مشتری"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_tbl.id"), nullable=False)
    edit_status = Column(Boolean, default=False, nullable=False)
    visit_status = Column(Boolean, default=False, nullable=False) 
    visit_Date = Column(DateTime, nullable=True)
    user_idit_data = Column(DateTime, nullable=True)
    server_idit_data = Column(DateTime, nullable=True, onupdate=func.now())
    
    customer = relationship("Customer", back_populates="visit_reports")
    user = relationship("User", back_populates="visit_reports")