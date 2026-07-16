from typing import Optional
from pydantic import BaseModel
from app.utils.constans import RoleName

class User(BaseModel):
    username: str 
    first_name : str
    last_name : str
    password : str
    isactive : bool
    role: Optional[RoleName] = None # استفاده از نام نقش به جای آیدی
