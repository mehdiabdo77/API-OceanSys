from app.core.base import Base 

from sqlalchemy.orm import Session
from app.models.user.user_model import UserModel
from app.models.user.permission_model import PermissionModel
from app.models.user.role_permission_model import RolePermissionModel
from app.models.user.user_permission_model import UserPermissionModel, GrantType

def user_has_permission(session: Session, user_id: int, permission_code: str) -> bool:
    """
    بررسی می‌کند که آیا کاربر مجوز خاصی دارد یا نه
    (با درنظر گرفتن نقش و استثناهای ALLOW/DENY)
    """
    # پیدا کردن مجوز مورد نظر
    permission = session.query(PermissionModel).filter_by(code=permission_code).first()
    if not permission:
        return False
    permission_id = permission.id

    # بررسی DENY
    deny = session.query(UserPermissionModel).filter_by(user_id=user_id, permission_id=permission_id, grant_type=GrantType.DENY).first()
    if deny:
        return False

    # بررسی نقش کاربر
    user = session.query(UserModel).filter_by(id=user_id).first()
    if user:
        role_permission = session.query(RolePermissionModel).filter_by(role_id=user.role_id, permission_id=permission_id).first()
        if role_permission:
            return True

    # بررسی ALLOW مستقیم
    allow = session.query(UserPermissionModel).filter_by(user_id=user_id, permission_id=permission_id, grant_type=GrantType.ALLOW).first()
    if allow:
        return True

    return False
