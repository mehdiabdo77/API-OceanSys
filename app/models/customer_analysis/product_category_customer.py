
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base



class ProductCategoryCustomerModel(Base):
     __tablename__ = "ProductCategoryCustomer"

     id = Column(Integer, primary_key=True, autoincrement=True) 
     customer_code = Column(Integer,nullable=False )  
     sku = Column(String(100), nullable=False)    
     user_id = Column(Integer, ForeignKey("user_tbl.id"), nullable=False)
     created_at = Column(DateTime, nullable=True)

     # رابطه با کاربر
     user = relationship("UserModel", backref="product_category_customers")