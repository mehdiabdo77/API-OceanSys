from sqlalchemy import Column, Integer, String
from app.core.base import Base

class LocationTypeModel(Base):
    """جدول مرجع نوع محل فعالیت"""
    __tablename__ = "LocationType"
    __table_args__ = {"schema": "Scanner"}

    LocationTypeID = Column(Integer, primary_key=True, autoincrement=False, comment="شناسه نوع محل فعالیت")
    LocationTypeName = Column(String(50), nullable=False, unique=True, comment="نام نوع محل فعالیت")
