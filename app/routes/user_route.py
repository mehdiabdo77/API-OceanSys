from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy import null
from app.auth.auth_handler import get_current_user
from app.schemas.response_schemas import UserModel
from app.services.user_service import Countuser, getUserDB , saveUserDB
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user_schemas import User

user_router = APIRouter()


@user_router.get("/getUserdata", response_model=UserModel)
def get_user_data(username: str = Depends(get_current_user)):
    user = getUserDB(username)
    return user


#TODO باید کاری کنم که فقط افرادی که دسترسی میدم بتونند یوزر تعریف کنن
@user_router.post("/register")
def register_user(data: User, username: str = Depends(get_current_user)):
    if username is not null :
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
