from fastapi import Depends, HTTPException, status
from app.auth.auth_handler import get_current_user
from app.services.permission_service import user_has_permission

def permission_required(permission_code : str):
     """
    Dependency برای بررسی داشتن مجوز خاص توسط کاربر
    """
     def wrapper(user_id = Depends(get_current_user)):
          try:
               if not user_has_permission( user_id, permission_code):
                    raise HTTPException(
                     status_code=status.HTTP_403_FORBIDDEN,
                     detail=f"Access denied: missing permission '{permission_code}'"
                 )
               return user_id # PermissionCheck(has_access=True, user_id=current_user.id)
          except Exception as e:
               print(f"Database error in save_point: {e}")
               return {"error": f"Failed to save point: {str(e)}"}
               
     return wrapper