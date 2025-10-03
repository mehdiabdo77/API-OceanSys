from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class CustomerIditModel(Base):
     __tablename__ = "CustomerIditTBL"
     customer_code = Column(Integer, primary_key=True, nullable=False)
     national_code = Column(String(12), nullable=True)
     role_code = Column(String(20), nullable=True)
     postal_code = Column(String(12), nullable=True)
     customer_board = Column(String(255), nullable=True)
     customer_name = Column(String(255), nullable=True)
     address = Column(Text, nullable=True)
     mobile_number = Column(String(20), nullable=True)
     mobile_number2 = Column(String(20), nullable=True)
     phone_number = Column(String(20), nullable=True)
     store_area = Column(Integer, nullable=True)
     user_id = Column(Integer, ForeignKey("user_tbl.id"), nullable=False)
     created_at = Column(DateTime, nullable=True)
     
     user = relationship("UserModel", backref="customer_edits")