from pydantic import BaseModel
from typing import Optional

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
    is_cooperation: bool
    
# تموم شدن کار    
class TaskComplete(BaseModel):
    customer_code: str 
    

class CustomerModel(BaseModel):
    customer_code: int 
    customer_name: str| None
    customer_board: str| None
    national_code: str
    area: str # محدودهغ
    zone: str # ناحیه
    route: str # مسیر
    latitude: float | str | None = None
    longitude: float  | str | None = None
    status: str
    address: str
    phone: str
    mobile: str | None
    postal_code: str | None
    username: str
    datavisit : Optional[str] = None
    visited : int
    edit : int
