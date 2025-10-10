from pydantic import BaseModel

class User(BaseModel):
    username: str 
    first_name : str
    last_name : str
    password : str
    isactive : bool
    role_id : int # (Foreign Key → role_tbl.id)
