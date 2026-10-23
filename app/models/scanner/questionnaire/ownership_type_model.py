from sqlalchemy import Column, Integer, String, CheckConstraint
from app.core.base import Base

class OwnershipTypeModel(Base):
    __tablename__ = "OwnershipType"
    __table_args__ = {"schema": "Scanner"}

    OwnershipTypeID = Column(Integer, primary_key=True, autoincrement=False)
    OwnershipTypeName = Column(String(50), nullable=False, unique=True)
