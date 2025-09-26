from pydantic import BaseModel
   
class Point(BaseModel):
    customer_code: str | None =None
    lat : float
    lng : float
    

class RouteUpdate(BaseModel):
    route_id: str
    username: int 
    visit_Date: str