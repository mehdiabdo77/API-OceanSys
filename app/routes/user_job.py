from fastapi import APIRouter , HTTPException , Depends
from app.schemas.customer_schemas import JobUserRequest
from app.auth.auth_handler import get_current_user
from app.services.job_user_service import set_job_user


job_user_router = APIRouter(tags=['job_user'])

@job_user_router.post("/set_rout")
def point(data: JobUserRequest, user_id: int = Depends(get_current_user)):
     if user_id is None:
          raise HTTPException(status_code=401, detail="Invalid credentials")
     else:
          result = set_job_user(data, user_id)
          if not result.get("success"):
               raise HTTPException(status_code=400, detail=result.get("error"))
          return result



@job_user_router.delete("/del_rout")
def del_rout(data: JobUserRequest, user_id: int = Depends(get_current_user)):
     if user_id is None:
          raise HTTPException(status_code=401, detail="Invalid credentials")
     else:
        #   result = some_delete_service(data, user_id)
          return {"message": "Not implemented yet"}

