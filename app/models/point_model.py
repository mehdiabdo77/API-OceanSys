from sqlalchemy import Column, Integer, String, DATETIME, DECIMAL
from sqlalchemy.orm import relationship
from app.models.base import Base


class PointModel(Base):
    __tablename__ = "Point_tbl"

    customer_code = Column(Integer, primary_key=True)
    lat = Column(DECIMAL(9,6), nullable=True)
    lng = Column(DECIMAL(9,6), nullable=True)
    username = Column(String(200), nullable=True)
    date_shamsi = Column(String(20), nullable=True)
    date_miladi = Column(DATETIME, nullable=True)
    
    
    



