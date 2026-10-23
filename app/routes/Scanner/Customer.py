from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from app.auth.auth_handler import get_current_user
from app.auth.permissions import permission_required
from app.services.customer_service import getCustomerInfo, sendDisActiveDescription , sendProductCategory , sendCRMCustomerDescription , update_customer_isvisit, save_customer_edit , update_customer_isedit
from app.schemas.customer_schemas import CustomerModel , CustomerEdit, DisActiveDescription, ProductCategory , CRMCustomerDescription , TaskComplete
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.constans import Permissions

customer_router = APIRouter(tags=['customer'])


@customer_router.get(
    "/getCustomerData",
    # response_model=List[CustomerModel]
    )
def get_customer_data( user_id = Depends(permission_required(Permissions.CUSTOMER_SCAN) )):
    """
    دریافت اطلاعات کامل مشتریان
    ---------------------------------
    این روت اطلاعات کامل مشتریان مرتبط با کاربر فعلی را برمی‌گرداند.
    نیاز به دسترسی CUSTOMER_SCAN دارد.
    
    Get complete customer information
    -----------------------------------
    This endpoint returns complete information of customers related to the current user.
    Requires CUSTOMER_SCAN permission.
    """
    if isinstance(user_id, dict) and "error" in user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    else:
        customerInfo = getCustomerInfo(user_id)
        return customerInfo




@customer_router.post("/editcoustomerinfo")
def editCustomerData( 
                     update_data: CustomerEdit,
                     user_id = Depends(permission_required(Permissions.CUSTOMER_SCAN))
                     ):
    """
    ویرایش اطلاعات مشتری
    ---------------------------------
    این روت برای ویرایش اطلاعات مشتری استفاده می‌شود.
    مراحل انجام:
    1. ذخیره تغییرات در جدول CustomerEditTable
    2. به‌روزرسانی وضعیت بازدید (isvisit) مشتری
    3. به‌روزرسانی وضعیت ویرایش (isedit) مشتری
    نیاز به دسترسی CUSTOMER_SCAN دارد.
    
    Edit customer information
    -----------------------------------
    This endpoint is used to edit customer information.
    Steps:
    1. Save changes to CustomerEditTable
    2. Update customer visit status (isvisit)
    3. Update customer edit status (isedit)
    Requires CUSTOMER_SCAN permission.
    """
    if isinstance(user_id, dict) and "error" in user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # ذخیره تغییرات در جدول CustomerIditTable
    result = save_customer_edit(update_data, user_id if not isinstance(user_id, dict) else user_id.get("user_id", 0))
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # به‌روزرسانی وضعیت بازدید مشتری
    visit_update = update_customer_isvisit(update_data.customer_code)
    print( visit_update)
    edit_update = update_customer_isedit(update_data.customer_code)
    print(edit_update)
    error = []
    if "error" in visit_update:
        error.append(visit_update["error"])
    if "error" in edit_update:
        error.append(edit_update["error"])
    if error:
        print(error)
        raise HTTPException(status_code=400, detail=" ".join(error))
    return {
        "message": result.get("message"), 
        "visit": visit_update.get("message"),
        "edit": edit_update.get("message")
    }
    
@customer_router.post("/disActiveCustomer")
def disActiveCustomer( 
                      disActiveData: DisActiveDescription ,
                      user_id = Depends(permission_required(Permissions.CUSTOMER_SCAN))
                      ):
    """
    غیرفعال کردن مشتری
    ---------------------------------
    این روت برای ثبت توضیحات و غیرفعال کردن مشتری استفاده می‌شود.
    مراحل انجام:
    1. ذخیره توضیحات غیرفعال‌سازی
    2. به‌روزرسانی وضعیت بازدید (isvisit) مشتری
    نیاز به دسترسی CUSTOMER_SCAN دارد.
    
    Deactivate customer
    -----------------------------------
    This endpoint is used to record description and deactivate a customer.
    Steps:
    1. Save deactivation description
    2. Update customer visit status (isvisit)
    Requires CUSTOMER_SCAN permission.
    """
    if isinstance(user_id, dict) and "error" in user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    else:
        result = sendDisActiveDescription(disActiveData , user_id if not isinstance(user_id, dict) else user_id.get("user_id", 0))
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    visit_update = update_customer_isvisit(int(disActiveData.customer_code))
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    return {"message": result.get("message"), "visit": visit_update.get("message")}
        

@customer_router.post("/ProductCategory")
def ProductCategoryCustomer( 
                            data: ProductCategory,
                            user_id = Depends(permission_required(Permissions.CUSTOMER_SCAN))
                            ):
    """
    ثبت دسته‌بندی محصولات برای مشتری
    ---------------------------------
    این روت برای ثبت دسته‌بندی محصولات و سوابق مرتبط با مشتری استفاده می‌شود.
    مراحل انجام:
    1. ذخیره دسته‌بندی محصولات و سوابق
    2. به‌روزرسانی وضعیت بازدید (isvisit) مشتری
    نیاز به دسترسی CUSTOMER_SCAN دارد.
    
    Record product categories for customer
    -----------------------------------
    This endpoint is used to record product categories and related history for a customer.
    Steps:
    1. Save product categories and history
    2. Update customer visit status (isvisit)
    Requires CUSTOMER_SCAN permission.
    """
    if isinstance(user_id, dict) and "error" in user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    else:
            result = sendProductCategory(data, user_id if not isinstance(user_id, dict) else user_id.get("user_id", 0))
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    visit_update = update_customer_isvisit(int(data.customer_code))
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    return {"message": result.get("message"), "visit": visit_update.get("message")}
        

@customer_router.post("/CRMCustomerDescription")
def crmCustomerDescription ( 
                            data: CRMCustomerDescription,
                            user_id = Depends(permission_required(Permissions.CUSTOMER_SCAN))
                            ):
    """
    ثبت توضیحات CRM مشتری
    ---------------------------------
    این روت برای ثبت توضیحات و یادداشت‌های مربوط به CRM برای مشتری استفاده می‌شود.
    مراحل انجام:
    1. ذخیره توضیحات CRM مشتری
    2. به‌روزرسانی وضعیت بازدید (isvisit) مشتری
    نیاز به دسترسی CUSTOMER_SCAN دارد.
    
    Record CRM customer description
    -----------------------------------
    This endpoint is used to record CRM-related descriptions and notes for a customer.
    Steps:
    1. Save CRM customer description
    2. Update customer visit status (isvisit)
    Requires CUSTOMER_SCAN permission.
    """
    if isinstance(user_id, dict) and "error" in user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    else:
        result = sendCRMCustomerDescription(data , user_id if not isinstance(user_id, dict) else user_id.get("user_id", 0))  
    visit_update = update_customer_isvisit(int(data.customer_code))
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result



@customer_router.post("/task_complete")
def task_complete ( data: TaskComplete, username: str = Depends(get_current_user)):
    """
    تکمیل وظیفه/بازدید مشتری
    ---------------------------------
    این روت برای علامت‌گذاری وظیفه/بازدید مشتری به عنوان تکمیل شده استفاده می‌شود.
    مراحل انجام:
    1. به‌روزرسانی وضعیت بازدید (isvisit) مشتری با پارامتر تکمیل
    نیاز به احراز هویت دارد (برخلاف سایر روت‌های مشتری، نیازی به دسترسی CUSTOMER_SCAN نیست).
    
    Complete customer task/visit
    -----------------------------------
    This endpoint is used to mark a customer task/visit as completed.
    Steps:
    1. Update customer visit status (isvisit) with complete parameter
    Requires authentication (unlike other customer endpoints, does not require CUSTOMER_SCAN permission).
    """
    if username is None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        visit_update = update_customer_isvisit(int(data.customer_code),1)
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    return visit_update

