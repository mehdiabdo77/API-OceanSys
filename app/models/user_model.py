from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = "user_tbl"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    department_id = Column(Integer, ForeignKey("department_tbl.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("position_tbl.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at_jalali = Column(String(10), nullable=False)
    updated_at_jalali = Column(String(10), nullable=False)

    visit_reports = relationship("VisitReport", back_populates="user")
