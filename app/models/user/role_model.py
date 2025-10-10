from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.models.user.role_permission_model import RolePermissionModel

class RoleModel(Base):
     __tablename__ = "role_tbl"

     id = Column(Integer, primary_key=True, autoincrement=True)
     name = Column(String(100), unique=True, nullable=False)
     description = Column(Text, nullable=True)
     created_at = Column(DateTime, default=func.now())

     users = relationship("app.models.user.user_model.UserModel", back_populates="role")
     permissions = relationship("app.models.user.role_permission_model.RolePermissionModel", back_populates="role")