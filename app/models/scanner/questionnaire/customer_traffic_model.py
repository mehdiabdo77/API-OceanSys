from sqlalchemy import Column, Integer, String
from app.core.base import Base

class CustomerTrafficModel(Base):
    __tablename__ = "CustomerTraffic"
    __table_args__ = {"schema": "Scanner"}

    CustomerTrafficID = Column(Integer, primary_key=True, autoincrement=False)
    CustomerTrafficName = Column(String(50), nullable=False, unique=True)
