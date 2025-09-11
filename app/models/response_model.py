from typing import Optional, Union
from pydantic import BaseModel

class UserModel(BaseModel):
    id: int
    user: str
    position: str
    
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

class VisitCreate(BaseModel):
    customer_code: int
    visit_date: str
    visited: bool
    visitor_username: str
    notes: Optional[str] = None

class EditCreate(BaseModel):
    customer_code: int
    editor_username: str
    original_data: dict
    edited_data: dict
    notes: Optional[str] = None
    
    
   
