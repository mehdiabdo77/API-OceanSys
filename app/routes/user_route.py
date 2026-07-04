from fastapi import APIRouter, Body, Depends, HTTPException
from app.auth.auth_handler import get_current_user
from app.auth.permissions import permission_required
from app.schemas.response_schemas import UserModel
from app.services.user_service import Countuser, getAllUsersDB, getUserDB, saveUserDB
from app.schemas.user_schemas import User
from app.utils.constans import Permissions

user_router = APIRouter(tags=['user'])


@user_router.post("/setup-first-user")
def register_first_user(data: User):
    """
    ایجاد کاربر اول سیستم

    Create the first user of the system
    
    فقط زمانی کار می‌کند که سیستم هیچ کاربری نداشته باشد

    Only works when the system has no users yet
    """
    count = Countuser()
    if isinstance(count, int) and count == 0:
        result = saveUserDB(data)
        if result["message"] == "successfully":
            return {
                "success": True,
                "message": "کاربر اول با موفقیت ایجاد شد",
                "data": result
            }
        else:
            raise HTTPException(status_code=400, detail="Error in saving user")
    else:
        raise HTTPException(status_code=400, detail="Already have a first user")


@user_router.post("/register")
def register_user(
            data: User,
            user_id: str = Depends(permission_required(Permissions.USER_MANAGE))
            ):
    """
    ثبت کاربر جدید

    Register a new user
    
    نیاز به دسترسی USER_MANAGE دارد

    Requires USER_MANAGE permission
    """
    if isinstance(user_id, dict) and "error" in user_id:
        result = saveUserDB(data)
        return {
            "success": True,
            "message": "کاربر با موفقیت ایجاد شد",
            "data": result
        }
    else:
        raise HTTPException(status_code=400, detail="You are not authorized to register users")


@user_router.get("/getUserdata", response_model=UserModel)
def get_user_data(user_id=Depends(get_current_user)):
    """
    دریافت اطلاعات کاربر فعلی

    Get current user information
    
    نیاز به احراز هویت دارد

    Requires authentication
    """
    user = getUserDB(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/getAllUserdata", response_model=list[UserModel])
def get_all_user_data(
        user_id: str = Depends(permission_required(Permissions.USER_MANAGE))
        ):
    """
    دریافت لیست تمام کاربران

    Get list of all users
    
    نیاز به دسترسی USER_MANAGE دارد

    Requires USER_MANAGE permission
    """
    users = getAllUsersDB()
    if isinstance(users, dict) and "error" in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users
