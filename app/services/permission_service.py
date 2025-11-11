from operator import and_
from fastapi import HTTPException
from sqlalchemy import Case, false
from app.core.base import SessionLocal 
from sqlalchemy.orm import aliased, query
from app.models.user.role_model import RoleModel
from app.models.user.user_model import UserModel
from app.models.user.permission_model import PermissionModel
from app.models.user.role_permission_model import RolePermissionModel
from app.models.user.user_permission_model import UserPermissionModel, GrantType
from sqlalchemy import case, literal
from sqlalchemy.sql import expression

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
def update_user_permissions(
    user_id: int,
    permissions_list: list[dict] # [{'permission': 'CUSTOMER_SCAN', 'grant_type': 'ALLOW'}, {'permission': 'CUSTOMER_REGISTER', 'grant_type': 'DENY'}]
    ):
    """
    بروزرسانی دسترسی‌های کاربر بر اساس لیست دسترسی‌های ارسالی
    هر آیتم در لیست شامل permission و grant_type است
    """
    db = None
    try:
        db = SessionLocal()
        # دریافت نقش کاربر
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return {"error": "کاربر یافت نشد"}
        
        # گرفتن نقش کاربر بدون بررسی دسترسی خاص
        quaryresult = db.query(
                PermissionModel.code,
                case(
                    (RolePermissionModel.permission_id != None, literal("ALLOW")),
                    else_=literal("DENY")
                )
            )\
            .select_from(PermissionModel)\
            .outerjoin(
                RolePermissionModel,
                expression.and_(
                    RolePermissionModel.permission_id == PermissionModel.id,
                    RolePermissionModel.role_id == user.role_id
                )
            )\
            .all()

        # خروجی من یه لیست از دیکشنری
        existing_permission_role =  {
            p : has_access
            for p, has_access in quaryresult
        }
        
        for permission_item in permissions_list:
            permission = permission_item.get("permission")
            grant_type = permission_item.get("grant_type")
            
            if not permission or not grant_type:
                return {"error": str(f"اطلاعات دسترسی {permission} ناقص است")}
                
            # دریافت شناسه دسترسی
            permission_record = db.query(PermissionModel.id).filter(PermissionModel.code == permission).first()
            if not permission_record:
                return {"error": str(f"دسترسی {permission} یافت نشد")}
                
            permission_id = permission_record[0]  # استخراج مقدار ID از نتیجه کوئری
            
            # بررسی وجود دسترسی قبلی
            existing_perm = db.query(UserPermissionModel).filter_by(
                user_id=user_id,
                permission_id=permission_id
            ).first()
            
            # از دیکشنری که ساخته بودم دسترسی میگیرم 
            role_access = existing_permission_role.get(permission)
                    
            if role_access != grant_type:
                if existing_perm:
                    existing_perm.grant_type = GrantType[grant_type]  # pyright: ignore[reportAttributeAccessIssue]
                else:
                    db.add(UserPermissionModel(
                        user_id=user_id,
                        permission_id=permission_id,
                        grant_type=GrantType(grant_type)
                    ))
            else  :
                if existing_perm:
                    db.delete(existing_perm)
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
            

def update_role_permissions(
    role: str,
    permissions_list: list[dict] # [{'permission': 'CUSTOMER_SCAN', 'grant_type': 'ALLOW'}, {'permission': 'CUSTOMER_REGISTER', 'grant_type': 'DENY'}]
    ):
    db = SessionLocal();
    
    try:
        db = SessionLocal()
        role = db.query(RoleModel).filter_by(name=role).first()
        if not role:
            return {"error": "نقش یافت نشد"}

        # دریافت همه‌ی دسترسی‌ها و وضعیتشان برای این نقش
        quaryresult = (
            db.query(
                PermissionModel.code,
                case(
                    (
                        db.query(RolePermissionModel)
                        .join(RoleModel, RoleModel.id == RolePermissionModel.role_id)
                        .filter(
                            RolePermissionModel.permission_id == PermissionModel.id,
                            RoleModel.name == role.name
                        )
                        .exists(),
                        literal("ALLOW")
                    ),
                    else_=literal("DENY")
                ).label("has_access")
            )
            .select_from(PermissionModel)
            .order_by(PermissionModel.code)
        )

        results = quaryresult.all() #[('COMPETITOR_PRICES', 1), ('CUSTOMER_SCAN', 1), ('FINANCE_REPORTS', 0), ('NEW_CUSTOMER', 1), ('UPLOAD_DATA', 1), ('USER_MANAGE', 0), ('VIEW_DASHBOARD', 1)]
        
        existing_permission_role =  {
            p : has_access
            for p, has_access in results
        }
        
        # فیلد ادیت 
        for permission_item in permissions_list:
            permission = permission_item.get("permission")
            grant_type = permission_item.get("grant_type")
            
            if not permission or not grant_type:
                return {"error": str(f"اطلاعات دسترسی {permission} ناقص است")}
                
            # دریافت شناسه دسترسی
            permission_record = db.query(PermissionModel.id).filter(PermissionModel.code == permission).first()
            if not permission_record:
                return {"error": str(f"دسترسی {permission} یافت نشد")}
            
            permission_role_filter = db.query(RolePermissionModel).filter_by(
                role_id=role.id,
                permission_id=permission_record[0]
            ).first()
        
            perCheack = existing_permission_role.get(permission)
            
            if grant_type == "ALLOW" and not permission_role_filter:
                db.add(RolePermissionModel(role_id=role.id, permission_id=permission_record[0]))
            elif grant_type == "DENY" and permission_role_filter:
                db.delete(permission_role_filter)   
        
        db.commit()
        data = [{"code": code, "has_access": bool(has_access)} for code, has_access in results]
        return {"status": True, "data": data}

    except Exception as e:
        if db:
            db.rollback()
        print(f"Error fetching role permissions: {str(e)}")
        return {"error": str(e)}
    finally:
        if db:
            db.close()
            
def get_role():
    db = None
    try:
        db = SessionLocal()
        role = db.query(RoleModel).all()
        print(role)
        return role
    except Exception as e:
        if db:
            db.rollback()
        print(f"Error updating user permissions: {str(e)}")
        return {"error": str(e)}
    finally:
        if db:
            db.close()
    