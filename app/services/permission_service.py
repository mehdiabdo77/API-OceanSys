from operator import and_
from sqlalchemy import Case, false
from app.core.base import SessionLocal 
from sqlalchemy.orm import aliased, query
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


def get_all_permission_user(user_id: int) :
    """
    بررسی می‌کند که آیا کاربر مجوز خاصی دارد یا نه
    (با درنظر گرفتن نقش و استثناهای ALLOW/DENY)
    """
    session = None
    results = ""
    try:
        session = SessionLocal()
        u = aliased(UserModel)
        up = aliased(UserPermissionModel)
        rp = aliased(RolePermissionModel)
        p = aliased(PermissionModel)
        
        query = session.query(
            p.code,
            Case(
                (up.grant_type == GrantType.DENY, 0 ),
                (up.grant_type == GrantType.ALLOW, 0 ),
                (rp.permission_id != None, 1),
             else_ =0).label("has_access")
        ).select_from(p)\
        .outerjoin(u , u.id == user_id)\
        .outerjoin(up , and_(up.permission_id==p.id , up.user_id == u.id))\
        .outerjoin(rp , and_(rp.permission_id == p.id , rp.role_id == u.role_id))
        
        results = query.all()
        data = [{"code": code, "has_access": has_access} for code, has_access in results]
        return {"status": True, "data": data}
    except Exception as e:
        print(f"Database error in save_point: {e}")
        return {"status" : False}
    finally:
        if session is not None:
            session.close()

# TODO باید کاری کنم اگر دسترسی هست دیتا اضافی نریزه      
def update_user_permissions(user_id: int, permissions_list: list[dict]):
    """
    بروزرسانی دسترسی‌های کاربر بر اساس لیست دسترسی‌های ارسالی
    هر آیتم در لیست شامل permission_id و grant_type است
    """
    db = None
    try:
        db = SessionLocal()
        
        for permission_item in permissions_list:
            permission_id = permission_item.get("permission_id")
            grant_type = permission_item.get("grant_type")
            
            # بررسی وجود دسترسی قبلی
            existing_permission = db.query(UserPermissionModel).filter_by(
                user_id=user_id,
                permission_id=permission_id
            ).first()
            
            if existing_permission:
                # بروزرسانی نوع دسترسی اگر تو جدول دسترسی یوزر وجود نداشت 
                existing_permission.grant_type = GrantType(grant_type)  # pyright: ignore[reportAttributeAccessIssue]
                db.commit()
            else:
                # ایجاد دسترسی جدید
                new_permission = UserPermissionModel(
                    user_id=user_id,
                    permission_id=permission_id,
                    grant_type=GrantType(grant_type)
                )
                db.add(new_permission)
                db.commit()
                
        return {"message": "دسترسی‌های کاربر با موفقیت بروزرسانی شد"}
    except Exception as e:
        if db:
            db.rollback()
        print(f"Error updating user permissions: {str(e)}")
        return {"error": str(e)}
    finally:
        if db:
            db.close()