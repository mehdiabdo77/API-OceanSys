from pydantic import BaseModel

class User(BaseModel):
    username: str 
    fullName : str
    password : str
    isactive : bool
    departmentID : int # (Foreign Key → Department.id)
    positionID : int # (Foreign Key → Position.id) #TODO جدول باید طراحی کنی