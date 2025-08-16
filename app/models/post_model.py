from typing import Optional, Union
from pydantic import BaseModel

class CustomerEditModel(BaseModel):
    customer_code: int
    nationalCode: str | None = None
    roleCode: int | None = None
    postalCode: str | None = None
    customerboard: str | None = None  # customer_board در جدول
    custumername: str | None = None   # customer_name در جدول
    address: str | None = None
    mobileNumber: str | None = None   # mobile_number در جدول
    mobileNumber2: str | None = None  # mobile_number2 در جدول
    phoneNumber: str | None = None    # phone_number در جدول
    storeArea: int | None = None      # store_area در جدول
    
    


class DisActiveDescription(BaseModel):
    customer_code: str 
    Reason: str
    Description: str
    
class ProductCategory(BaseModel):
    customer_code: str 
    sku: list;
    
    
class CRMCustomerDescription(BaseModel):
    customer_code: str 
    Description: str
    is_customer_visit: bool       # آیا مشتری (فروشنده) خودش ویزیت/سرکشی می‌کند؟
    is_owner_in_shop: bool        # آیا صاحب مغازه در مغازه هست؟
    
    
    
class Point(BaseModel):
    customer_code: str | None =None
    lat : float
    lng : float

    