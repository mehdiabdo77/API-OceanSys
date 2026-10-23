from sqlalchemy import Column, Integer, String
from app.core.base import Base

class CustomerTrafficModel(Base):
    """جدول مرجع میزان مراجعه مشتریان"""
    __tablename__ = "CustomerTraffic"
    __table_args__ = {"schema": "Scanner"}

    CustomerTrafficID = Column(Integer, primary_key=True, autoincrement=False, comment="شناسه میزان مراجعه مشتریان")
    CustomerTrafficName = Column(String(50), nullable=False, unique=True, comment="سطح مراجعه مشتریان")
