from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from app.core.base import Base

class DisActiveDescriptionModel(Base):
    __tablename__ = "DeactivationReason"
    __table_args__ = {"schema": "Scanner"}

    customer_code = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Security.UserAccount.id"), nullable=False)
    Reason = Column(String(255), nullable=False)
    Description = Column(Text, nullable=True)
    created_at = Column(DateTime)
    
    # ارتبات با جدول یوزر
    user = relationship("UserModel", backref="disactive_descriptions")
    