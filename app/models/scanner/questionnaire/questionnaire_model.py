from sqlalchemy import Column, BigInteger, Integer, String, Numeric, Boolean, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.core.base import Base

class QuestionnaireModel(Base):
    __tablename__ = "Questionnaire"
    __table_args__ = {"schema": "Scanner"}

    QuestionnaireID = Column(BigInteger, primary_key=True, autoincrement=True)
    CustomerID = Column(BigInteger, nullable=False)
    VisitID = Column(BigInteger, nullable=True)
    StoreType = Column(String(50), nullable=True)
    OwnershipTypeID = Column(Integer, ForeignKey("Scanner.OwnershipType.OwnershipTypeID"), nullable=True)
    TotalArea = Column(Numeric(10, 2), nullable=True)
    BranchCount = Column(Integer, nullable=True)
    LocationTypeID = Column(Integer, ForeignKey("Scanner.LocationType.LocationTypeID"), nullable=True)
    CustomerTrafficID = Column(Integer, ForeignKey("Scanner.CustomerTraffic.CustomerTrafficID"), nullable=True)
    DeliveryCapability = Column(Boolean, nullable=True)
    SalesPotentialID = Column(Integer, ForeignKey("Scanner.SalesPotential.SalesPotentialID"), nullable=True)
    HasShelf = Column(Boolean, nullable=True)
    HasRefrigerator = Column(Boolean, nullable=True)
    InspectorNotes = Column(String(1000), nullable=True)
    CreatedAt = Column(DateTime, nullable=False, server_default=func.sysdatetime())
    CreatedBy = Column(BigInteger, nullable=True)

    ownership_type = relationship("OwnershipTypeModel", backref="questionnaires")
    location_type = relationship("LocationTypeModel", backref="questionnaires")
    customer_traffic = relationship("CustomerTrafficModel", backref="questionnaires")
    sales_potential = relationship("SalesPotentialModel", backref="questionnaires")
