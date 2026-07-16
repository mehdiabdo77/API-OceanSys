from fastapi import APIRouter, Body, Depends, HTTPException
from app.auth.auth_handler import get_current_user
from app.auth.permissions import permission_required
from app.schemas.response_schemas import UserModel
from app.services.user_service import Countuser, getAllUsersDB, getUserDB, saveUserDB, set_user_status
from app.services.permission_service import get_or_create_admin_role
from app.schemas.user_schemas import User
from app.utils.constans import Permissions

user_router = APIRouter(tags=['user'])


@user_router.patch("/{username}/status")
def toggle_user_status(
    username: str,
    is_active: bool,
    admin_id: str = Depends(permission_required(Permissions.USER_MANAGE))
):
    """
    فعال یا غیرفعال کردن کاربر بر اساس نام کاربری
    """
    if isinstance(admin_id, dict) and "error" in admin_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    result = set_user_status(username, is_active)
    if result["message"] == "successfully":
        return {"success": True, "message": "وضعیت کاربر با موفقیت تغییر کرد"}
    elif result["message"] == "User not found":
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    else:
        raise HTTPException(status_code=400, detail=result["message"])


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
        # ایجاد یا دریافت نقش ADMIN
        admin_role = get_or_create_admin_role()
        if "error" in admin_role:
            raise HTTPException(status_code=400, detail=admin_role["error"])
        
        admin_role_id = admin_role["role_id"]
        
        # ذخیره کاربر با نقش ADMIN
        result = saveUserDB(data, role_id=admin_role_id)
        if result["message"] == "successfully":
            return {
                "success": True,
                "message": "کاربر اول با موفقیت ایجاد شد و به نقش ADMIN اختصاص داده شد",
                "data": result,
                "role": admin_role
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
    if not isinstance(user_id, dict) or "error" not in user_id:
        result = saveUserDB(data)
        
        if isinstance(result, dict) and result.get("message") == "username_already_exists":
            raise HTTPException(status_code=400, detail="نام کاربری تکراری است")
        
        if isinstance(result, dict) and result.get("message") == "User saved unsuccessfully":
            raise HTTPException(status_code=500, detail="خطا در ذخیره کاربر")
            
        return {
            "success": True,
            "message": "کاربر با موفقیت ایجاد شد",
            "data": result
        }
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to register users")


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
