from app.core.base import Base, SessionLocal 
from sqlalchemy.orm import Session
from app.models.user.user_model import UserModel
from app.models.user.permission_model import PermissionModel
from app.models.user.role_permission_model import RolePermissionModel
from app.models.user.user_permission_model import UserPermissionModel, GrantType

def user_has_permission( user_id: int, permission_code: str) -> bool:
    """
    بررسی می‌کند که آیا کاربر مجوز خاصی دارد یا نه
    (با درنظر گرفتن نقش و استثناهای ALLOW/DENY)
    """
    session = None
    
    try :
        session = SessionLocal()
        
        # از روی متن ایدی مجوز پیدا میکنم مثلا دسترسی اصلاح مسیر ایدیش میشه 2
        permission = session.query(PermissionModel).filter_by(code=permission_code).first()
        print(f"permission {permission.description if permission else None}")
        if not permission:
            return False
        permission_id = permission.id

        # بررسی عدم دسترسی یوزر
        deny = session.query(UserPermissionModel).filter_by(
                                                        user_id=user_id,
                                                        permission_id=permission_id,
                                                        grant_type=GrantType.DENY
                                                        ).first()
        print(f"deny{deny}")
        if deny:
            return False

        # با بررسی ایدی کاربر و  دسترسی کامل هم داشته باشم  اینجا چک میکنم
        user = session.query(UserModel).filter_by(id=user_id).first()
        if user:
            role_permission = session.query(RolePermissionModel).filter_by(
                                            role_id=user.role_id,
                                            permission_id=permission_id
                                            ).first()
            if role_permission:
                return True

        # تو اینجا بررسی میکنم که ایا دسترسی خاص دارم یا نه
        allow = session.query(UserPermissionModel).filter_by(
                                            user_id=user_id,
                                            permission_id=permission_id,
                                            grant_type=GrantType.ALLOW
                                            ).first()
        if allow:
            return True

        return False
    except Exception as e:
        print(f"Database error in save_point: {e}")
        return False
    finally:
        if session is not None:
            session.close()


def edit_user_permission():
    pass