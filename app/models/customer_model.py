from sqlalchemy import Column, Integer, String, Text, DECIMAL
from sqlalchemy.orm import relationship
from app.core.base import Base

class CustomerModel(Base):
    __tablename__ = "customer"

    customer_code = Column(Integer, primary_key=True)
    customer_name = Column(String(150), nullable=False)
    customer_board = Column(String(150), nullable=False)
    national_code = Column(String(20), nullable=True)
    area = Column(String(20), nullable=False)
    zone = Column(String(20), nullable=False)
    route = Column(String(20), nullable=False)
    latitude = Column(DECIMAL(9, 6), nullable=True)
    longitude = Column(DECIMAL(9, 6), nullable=True)
    status = Column(String(10), nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String(11), nullable=True)
    mobile = Column(String(11), nullable=True)
    mobile2 = Column(String(11), nullable=True)
    postal_code = Column(String(12), nullable=True)
    
    image_address = Column(Text, nullable=True , default="")

    visit_reports = relationship("VisitReportModel", back_populates="customer")
