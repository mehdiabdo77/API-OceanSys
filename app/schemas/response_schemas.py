from typing import Optional, Union
from pydantic import BaseModel

class UserModel(BaseModel):
    # id: int
    username: str
    first_name: str
    last_name: str
    is_active : bool
    position_id : int
    department_id : int

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
    
    
   
