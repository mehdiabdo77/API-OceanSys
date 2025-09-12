from token import RIGHTSHIFT
from app.auth.auth_handler import get_current_user
from app.models import response_model
from app.models.post_model import RouteUpdate
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.db.route_repository import get_routes , add_user_route

visit_router = APIRouter()


@visit_router.get("/routes" , response_model =List | None)
def list_routes(username : str = Depends(get_current_user)):
     """
     دریافت لیست تمام مسیر های موجود
     """
     if username is None:
          raise HTTPException(status_code=401 , detail="Invalid credentials" )
     
     routes =get_routes()
     
     if routes is not None and "error" in routes:
        raise HTTPException(status_code=400, detail=result["error"])
   
     return routes


@visit_router.post("/update-route" )
def update_route ( data: RouteUpdate , username: str = Depends(get_current_user)):
     """
     اپدیت مسیر فروشنده 
     """
     if username is None:
          raise HTTPException(status_code=401 , detail="Invalid credentials" )
     result = add_user_route(data.route_id , username , data.datetime)
     
     if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
     return result