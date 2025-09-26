from fastapi import APIRouter , HTTPException , Depends
from app.schemas.post_schemas import Point
from app.auth.auth_handler import get_current_user
from app.services.point_service import save_point


point_router = APIRouter()

@point_router.post("/point")
def point(data: Point, username: str = Depends(get_current_user)):
     if username is None:
          raise HTTPException(status_code=401, detail="Invalid credentials")
     else:
          result = save_point(data, username)
          return result




