from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str 
    first_name : str
    last_name : str
    password : str
    isactive : bool
    role_id : Optional[int] = None # (Foreign Key → role_tbl.id)
