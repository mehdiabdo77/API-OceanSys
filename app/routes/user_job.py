from fastapi import APIRouter , HTTPException , Depends
from app.auth.permissions import permission_required
from app.schemas.customer_schemas import JobUserRequest
from app.auth.auth_handler import get_current_user
from app.services.job_user_service import del_job_user, set_job_user
from app.utils.constans import Permissions


job_user_router = APIRouter(tags=['job_user'])

@job_user_router.post("/set_rout")
def set_rout(
     data: JobUserRequest, 
     permission=Depends(permission_required(Permissions.JOB_ROUTE)),
     user_id: int = Depends(get_current_user)
     ):
    #  if user_id is None:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
     if isinstance(permission, dict) and "error" in permission:
        raise HTTPException(status_code=403, detail="Access denied")
     else:
        result = set_job_user(data)
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        return result



@job_user_router.delete("/del_rout")
def del_rout(
    data: JobUserRequest, 
    permission=Depends(permission_required(Permissions.JOB_ROUTE)),
    user_id: int = Depends(get_current_user)
     ):
    # if user_id is None:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    if isinstance(permission, dict) and "error" in permission:
        raise HTTPException(status_code=403, detail="Access denied")
    else:
        result = del_job_user(data)
        if not result.get("success"):
               raise HTTPException(status_code=400, detail=result.get("error"))
        return result

