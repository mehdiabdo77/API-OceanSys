from fastapi import Depends, HTTPException, status
from app.auth.auth_handler import get_current_user
from app.services.permission_service import user_has_permission
from app.core.base import SessionLocal

def permission_required(permission_code : str):
     """
    Dependency برای بررسی داشتن مجوز خاص توسط کاربر
    """
     def wrapper(current_user = Depends(get_current_user)):
          db = SessionLocal()
          try:
               if not user_has_permission(db, current_user, permission_code):
                    raise HTTPException(
                     status_code=status.HTTP_403_FORBIDDEN,
                     detail=f"Access denied: missing permission '{permission_code}'"
                 )
               return current_user
          finally:
               db.close()
     return wrapper