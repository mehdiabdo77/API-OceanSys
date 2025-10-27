from datetime import date
from typing import List
from fastapi import APIRouter, Body, Depends , HTTPException
from sqlalchemy import null
from app.auth.auth_handler import get_current_user
from app.auth.permissions import permission_required
from app.schemas.permission_schemas import PermissionEditSchemas
from app.schemas.response_schemas import UserModel
from app.services.permission_service import get_all_permission_user, update_user_permissions
from app.services.user_service import Countuser, getAllUsersDB, getUserDB , saveUserDB
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user_schemas import User
from app.utils.constans import Permissions

user_router = APIRouter()

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
    
    

@user_router.get("/getUserdata", response_model=UserModel)
def get_user_data(user_id  = Depends(get_current_user)):
    user = getUserDB(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/getAllUserdata" , response_model=list[UserModel])
def get_all_user_data(
        user_id: str =  Depends(permission_required(Permissions.USER_MANAGE) )
        ):
    users = getAllUsersDB()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@user_router.post("/get_permission")
def get_user_permission(user_id  = Depends(get_current_user)):
    result = get_all_permission_user(user_id)
    if result["status"] == True:
        return result ['data']
    else:
        raise HTTPException(status_code=400, detail="Error in getting permissions")


@user_router.put("/edit_permission")
def edit_user_permission(
            permission = Depends(permission_required(Permissions.USER_MANAGE)),
            datas: List[PermissionEditSchemas] = Body(...)
            ):
    try:
        if "error" in permission:
            raise HTTPException(status_code=403, detail="Access denied")
        
        results = []
        for data in datas:
            target_user_id = data.user_id
            permissions_list = data.permissions
            
            if not target_user_id or not permissions_list:
                raise HTTPException(status_code=400, detail="اطلاعات ناقص است")
            
            permissions_dict_list = [] # [{'permission': 'CUSTOMER_SCAN', 'grant_type': 'ALLOW'}, {'permission': 'CUSTOMER_REGISTER', 'grant_type': 'DENY'}]
            for perm in permissions_list:
                permissions_dict_list.append({
                    "permission": perm.permission,
                    "grant_type": perm.grant_type
                })
            result = update_user_permissions(int(target_user_id), permissions_dict_list)
            if "error" in result:
                results.append({"user_id": target_user_id, "status": "error", "message": result["error"]})
            else:
                results.append({"user_id": target_user_id, "status": "success", "message": result["message"]})
        
        return {"success": True, "results": results}
    except Exception as e:
        print(f"Error in edit_user_permission: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در بروزرسانی دسترسی‌ها: {str(e)}")