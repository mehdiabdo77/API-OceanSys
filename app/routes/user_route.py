from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy import null
from app.auth.auth_handler import get_current_user
from app.auth.permissions import permission_required
from app.schemas.response_schemas import UserModel
from app.services.permission_service import get_all_permission_user
from app.services.user_service import Countuser, getUserDB , saveUserDB
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user_schemas import User
from app.utils.constans import Permissions

user_router = APIRouter()


@user_router.get("/getUserdata", response_model=UserModel)
def get_user_data(user_id  = Depends(get_current_user)):
    user = getUserDB(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/getAllUserdata", response_model=UserModel)
def get_all_user_data(user_id =  Depends(permission_required(Permissions.USER_MANAGE) )):
    user = ""
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/register")
def register_user(
            data: User,
            user_id: str =  Depends(permission_required(Permissions.USER_MANAGE))
            ):
    if user_id is not null :
        result = saveUserDB(data)
        return {
            "success": True,
            "message": "کاربر با موفقیت ایجاد شد",
            "data": result
        }
    else :
        raise HTTPException(status_code=400, detail="You are not authorized to register users")
    
    
@user_router.post("/setup-first-user")
def register_first_user(data : User):
    count = Countuser()
    if isinstance(count, int) and count == 0:
        result = saveUserDB(data)
        if result["message"] == "successfully":
            return {
                "success": True,
                "message": "کاربر اول با موفقیت ایجاد شد",
                "data": result
            }
        else :
            raise HTTPException(status_code=400, detail="Error in saving user")
    else :
        raise HTTPException(status_code=400, detail="Already have a first user")

  
@user_router.post("/get_permission")
def get_user_permission(user_id  = Depends(get_current_user)):
    result = get_all_permission_user(user_id)
    if result["status"] == True:
        return result
    else:
        raise HTTPException(status_code=400, detail="Error in getting permissions")

