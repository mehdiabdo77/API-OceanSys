from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.models.customer_analysis.visit_report import VisitReportModel
from app.models.user.role_model import RoleModel
from app.models.user.user_permission_model import UserPermissionModel  # اضافه کردن این import

class UserModel(Base):
    __tablename__ = "user_tbl"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Integer, default=True)
    role_id = Column(Integer, ForeignKey("role_tbl.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    role = relationship(RoleModel, back_populates="users")
    permissions = relationship(UserPermissionModel, back_populates="user")
    visit_reports = relationship(VisitReportModel, back_populates="user")