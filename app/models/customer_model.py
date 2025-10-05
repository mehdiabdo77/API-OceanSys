from sqlalchemy import Column, Integer, String, Text, DECIMAL
from sqlalchemy.orm import relationship
from app.core.base import Base
# TODO اسم ستون ها دیتا بیس از فارسی به اینگلیسی تغییر بده تو اینده
class CustomerModel(Base):
    __tablename__ = "customer"

    کد_مشتری = Column(Integer, primary_key=True)
    نام_مشتری = Column(String(255), nullable=True)
    تابلو_مشستری = Column(String(255), nullable=True)
    کد_ملی = Column(String(20), nullable=True)
    محدوده = Column(String(100), nullable=True)
    ناحیه = Column(String(100), nullable=True)
    مسیر = Column(String(100), nullable=True)
    Latitude = Column(DECIMAL(9, 6), nullable=True)
    Longitude = Column(DECIMAL(9, 6), nullable=True)
    وضعیت = Column(String(50), nullable=True)
    آدرس_مشتری = Column(Text, nullable=True)
    تلفن_اول = Column(String(20), nullable=True)
    تلفن_همراه = Column(String(20), nullable=True)
    کد_پستی_مشتری = Column(String(20), nullable=True)

    visit_reports = relationship("VisitReportModel", back_populates="customer")
