from sqlalchemy import Column, BigInteger, Integer, String, Numeric, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.base import Base

class QuestionnaireModel(Base):
    """جدول اصلی پرسش‌نامه"""
    __tablename__ = "Questionnaire"
    __table_args__ = {"schema": "Scanner"}

    QuestionnaireID = Column(BigInteger, primary_key=True, autoincrement=True, comment="شناسه یکتای پرسش‌نامه")
    CustomerID = Column(BigInteger, nullable=False, comment="شناسه مشتری")
    VisitID = Column(BigInteger, nullable=True, comment="شناسه بازدید")
    StoreType = Column(String(50), nullable=True, comment="نوع فروشگاه")
    OwnershipTypeID = Column(Integer, ForeignKey("Scanner.OwnershipType.OwnershipTypeID"), nullable=True, comment="شناسه وضعیت مالکیت")
    TotalArea = Column(Numeric(10, 2), nullable=True, comment="مساحت کل محل به مترمربع")
    BranchCount = Column(Integer, nullable=True, comment="تعداد شعب کسب‌وکار")
    LocationTypeID = Column(Integer, ForeignKey("Scanner.LocationType.LocationTypeID"), nullable=True, comment="شناسه نوع محل فعالیت")
    CustomerTrafficID = Column(Integer, ForeignKey("Scanner.CustomerTraffic.CustomerTrafficID"), nullable=True, comment="شناسه میزان مراجعه مشتریان")
    DeliveryCapability = Column(Boolean, nullable=True, comment="امکان ارسال کالا: 1=بله، 0=خیر")
    SalesPotentialID = Column(Integer, ForeignKey("Scanner.SalesPotential.SalesPotentialID"), nullable=True, comment="شناسه پتانسیل فروش")
    HasShelf = Column(Boolean, nullable=True, comment="آیا فروشگاه شلف دارد؟ 1=بله، 0=خیر")
    HasRefrigerator = Column(Boolean, nullable=True, comment="آیا فروشگاه یخچال دارد؟ 1=بله، 0=خیر")
    InspectorNotes = Column(String(1000), nullable=True, comment="توضیحات تکمیلی بازرس")
    CreatedAt = Column(DateTime, nullable=False, server_default=func.sysdatetime(), comment="تاریخ و ساعت ثبت پرسش‌نامه")
    CreatedBy = Column(BigInteger, nullable=True, comment="شناسه کاربر ثبت‌کننده")

    ownership_type = relationship("OwnershipTypeModel", backref="questionnaires")
    location_type = relationship("LocationTypeModel", backref="questionnaires")
    customer_traffic = relationship("CustomerTrafficModel", backref="questionnaires")
    sales_potential = relationship("SalesPotentialModel", backref="questionnaires")
