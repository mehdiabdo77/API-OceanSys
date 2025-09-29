from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class VisitReport(Base):
    __tablename__ = "visit_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.کد_مشتری"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_tbl.id"), nullable=False)
    edit_status = Column(Boolean, default=False, nullable=False)
    visit_status = Column(Boolean, default=False, nullable=False)
    visit_Date = Column(DateTime, nullable=True)
    user_idit_data = Column(DateTime, nullable=True)
    server_idit_data = Column(DateTime, nullable=True, onupdate=func.now())

    customer = relationship("CustomerModel", back_populates="visit_reports")
    user = relationship("User", back_populates="visit_reports")
