from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from app.auth.permissions import permission_required
from app.schemas.permission_schemas import (
    PermissionRoleEditSchemas,
    PermissionUserEditSchemas,
    PermissionSchema,
    RoleCreateSchema,
    PermissionCreateSchema,
    RoleSchema
)
from app.services.permission_service import (
    get_all_permission_user,
    get_role,
    update_role_permissions,
    update_user_permissions,
    get_all_permissions,
    create_role,
    create_permission
)
from app.services.user_service import change_user_role
from app.auth.auth_handler import get_current_user
from app.utils.constans import Permissions

permission_router = APIRouter(tags=['permission'])


@permission_router.post("/get_permission")
def get_user_permission(user_id=Depends(get_current_user)):
    """
    دریافت دسترسی‌های کاربر فعلی

    Get current user permissions
    
    نیاز به احراز هویت دارد

    Requires authentication
    """
    result = get_all_permission_user(user_id)
    if result["status"] == True:
        return result['data']
    else:
        raise HTTPException(status_code=400, detail="Error in getting permissions")


@permission_router.put("/edit_permission_user")
def edit_user_permission(
            permission=Depends(permission_required(Permissions.USER_MANAGE)),
            datas: List[PermissionUserEditSchemas] = Body(...)
            ):
    """
    ویرایش دسترسی‌های یک یا چند کاربر

    Edit permissions of one or more users
    
    نیاز به دسترسی USER_MANAGE دارد

    Requires USER_MANAGE permission
    """
    try:
        if isinstance(permission, dict) and "error" in permission:
            raise HTTPException(status_code=403, detail="Access denied")
        
        results = []
        for data in datas:
            target_user_id = data.identifier
            permissions_list = data.permissions
            
            if not target_user_id or not permissions_list:
                raise HTTPException(status_code=400, detail="اطلاعات ناقص است")
            
            permissions_dict_list = []
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


@permission_router.put("/edit_permission_role")
def edit_role_permission(
            permission=Depends(permission_required(Permissions.USER_MANAGE)),
            datas: List[PermissionRoleEditSchemas] = Body(...)
            ):
    """
    ویرایش دسترسی‌های یک یا چند نقش

    Edit permissions of one or more roles
    
    نیاز به دسترسی USER_MANAGE دارد

    Requires USER_MANAGE permission
    """
    try:
        if isinstance(permission, dict) and "error" in permission:
            raise HTTPException(status_code=403, detail="Access denied")
        
        results = []
        for data in datas:
            target_role = data.identifier
            permissions_list = data.permissions
            
            if not target_role or not permissions_list:
                raise HTTPException(status_code=400, detail="اطلاعات ناقص است")
            
            permissions_dict_list = []
            
            for perm in permissions_list:
                permissions_dict_list.append({
                    "permission": perm.permission,
                    "grant_type": perm.grant_type
                })
                
            result = update_role_permissions(target_role, permissions_dict_list)
            
            if "error" in result:
                results.append({"role_name": target_role, "status": "error", "message": result["error"]})
            else:
                results.append({"role_name": target_role, "status": "success", "message": "دسترسی‌های نقش با موفقیت بروزرسانی شد"})
        
        return {"success": True, "results": results}
        
    except Exception as e:
        print(f"Error in edit_role_permission: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در بروزرسانی دسترسی‌ها: {str(e)}")


@permission_router.get("/get_role_list", response_model=list[RoleSchema])
def get_role_list(
            permission=Depends(permission_required(Permissions.USER_MANAGE)),
            ):
    """
    دریافت لیست نقش‌های سیستم

    Get list of system roles
    
    نیاز به دسترسی USER_MANAGE دارد
    
    Requires USER_MANAGE permission
    """
    try:
        if isinstance(permission, dict) and "error" in permission:
            raise HTTPException(status_code=403, detail="Access denied")
        
        results = get_role()
        if isinstance(results, dict) and "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return results
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in get_role_list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در  دریافت اطلاعت نقش ها: {str(e)}")


@permission_router.get("/get_permission_list", response_model=list[PermissionSchema])
def get_permission_list(
            permission=Depends(permission_required(Permissions.USER_MANAGE)),
            ):
    """
    دریافت لیست تمام دسترسی‌های سیستم

    Get list of all system permissions
    
    نیاز به دسترسی USER_MANAGE دارد
    
    Requires USER_MANAGE permission
    """
    try:
        if isinstance(permission, dict) and "error" in permission:
            raise HTTPException(status_code=403, detail="Access denied")
        
        results = get_all_permissions()
        if isinstance(results, dict) and "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return results
        
    except Exception as e:
        print(f"Error in get_permission_list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در دریافت لیست دسترسی‌ها: {str(e)}")


@permission_router.post("/create_role", response_model=RoleSchema)
def create_role_endpoint(
            data: RoleCreateSchema,
            permission=Depends(permission_required(Permissions.USER_MANAGE)),
            ):
    """
    ایجاد نقش جدید

    Create new role
    
    نیاز به دسترسی USER_MANAGE دارد
    
    Requires USER_MANAGE permission
    """
    try:
        if isinstance(permission, dict) and "error" in permission:
            raise HTTPException(status_code=403, detail="Access denied")
        
        result = create_role(data.name, data.description)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result["data"]
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in create_role_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در ایجاد نقش: {str(e)}")


@permission_router.post("/create_permission", response_model=PermissionSchema)
def create_permission_endpoint(
            data: PermissionCreateSchema,
            permission=Depends(permission_required(Permissions.USER_MANAGE)),
            ):
    """
    ایجاد دسترسی جدید

    Create new permission
    
    نیاز به دسترسی USER_MANAGE دارد
    
    Requires USER_MANAGE permission
    """
    try:
        if isinstance(permission, dict) and "error" in permission:
            raise HTTPException(status_code=403, detail="Access denied")
        
        result = create_permission(data.code, data.name, data.description)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result["data"]
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in create_permission_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در ایجاد دسترسی: {str(e)}")


@permission_router.patch("/change_user_role")
def change_user_role_endpoint(
    username: str,
    role_name: str,
    permission=Depends(permission_required(Permissions.USER_MANAGE))
):
    """
    تغییر نقش کاربر توسط ادمین
    """
    if isinstance(permission, dict) and "error" in permission:
        raise HTTPException(status_code=403, detail="Access denied")
    
    result = change_user_role(username, role_name)
    if result["message"] == "successfully":
        return {"success": True, "message": "نقش کاربر با موفقیت تغییر کرد"}
    elif result["message"] == "User not found":
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    elif result["message"] == "Role not found":
        raise HTTPException(status_code=404, detail="نقش یافت نشد")
    else:
        raise HTTPException(status_code=400, detail=result["message"])
