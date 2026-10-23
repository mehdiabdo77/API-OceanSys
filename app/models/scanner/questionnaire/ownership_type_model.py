from sqlalchemy import Column, Integer, String
from app.core.base import Base

class OwnershipTypeModel(Base):
    """جدول مرجع وضعیت مالکیت"""
    __tablename__ = "OwnershipType"
    __table_args__ = {"schema": "Scanner"}

    OwnershipTypeID = Column(Integer, primary_key=True, autoincrement=False, comment="شناسه وضعیت مالکیت")
    OwnershipTypeName = Column(String(50), nullable=False, unique=True, comment="نام وضعیت مالکیت")
