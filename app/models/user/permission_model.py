from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.core.base import Base

class PermissionModel(Base):
     __tablename__ = "permission_tbl"

     id = Column(Integer, primary_key=True, autoincrement=True)
     code = Column(String(100), unique=True, nullable=False)
     name = Column(String(100), nullable=False)
     description = Column(Text, nullable=True)
     created_at = Column(DateTime, default=func.now())

     users = relationship("UserPermissionModel", back_populates="permission")
     roles = relationship("RolePermissionModel", back_populates="permission")