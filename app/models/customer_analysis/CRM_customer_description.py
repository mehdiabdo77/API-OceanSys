from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base


class CRMCustomerDescriptionModel(Base):
    __tablename__ = "CRMCustomerDescription"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    customer_code = Column(Integer, nullable=False)  
    description_crm = Column(Text, nullable=False)
    is_customer_visit = Column(Boolean, default=False)  
    is_owner_in_shop = Column(Boolean, default=False)
    is_cooperation = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("user_tbl.id"), nullable=False)  
    
    created_at = Column(DateTime)

    user = relationship("UserModel", backref="CRM_customer_descriptions")
