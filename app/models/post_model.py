from typing import Optional, Union
from pydantic import BaseModel


    
class CustomerEditModel(BaseModel):
    customer_code: int 
    national_code: str
    area: str # محدوده
    zone: str # ناحیه
    route: str # مسیر
    latitude: float 
    longitude: float  
    status: str
    address: str
    phone: str
    mobile: str | None
    postal_code: str | None
    username: str
    datavisit : str
    visited : int
    edit : int
    dateVisit : int
    username : str

    
    