from sqlalchemy import Column, Integer, String
from app.core.base import Base

class SalesPotentialModel(Base):
    __tablename__ = "SalesPotential"
    __table_args__ = {"schema": "Scanner"}

    SalesPotentialID = Column(Integer, primary_key=True, autoincrement=False)
    SalesPotentialName = Column(String(50), nullable=False, unique=True)
