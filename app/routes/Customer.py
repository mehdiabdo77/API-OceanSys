from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from app.auth.auth_handler import get_current_user
from app.db.customer_repository import getCustomerInfo, sendDisActiveDescription , sendProductCategory , sendCRMCustomerDescription , update_customer_isvisit, save_customer_edit , update_customer_isedit
from app.models.response_model import CustomerModel
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.post_model import CustomerEditModel, DisActiveDescription, ProductCategory , CRMCustomerDescription , TaskComplete


customer_router = APIRouter()


@customer_router.get(
    "/getCustomerData",
    response_model=List[CustomerModel] 
    )
def get_customer_data(username: str = Depends(get_current_user) , ):
    """
    گرفتن اطلاعات کامل مشتری 
    """
    customerInfo = getCustomerInfo(username)
    return customerInfo




# TODO 
@customer_router.post("/editcoustomerinfo")
def editCustomerData( update_data: CustomerEditModel  , username: str = Depends(get_current_user)):
    if username == None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # ذخیره تغییرات در جدول CustomerIditTabel
    result = save_customer_edit(update_data, username)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # به‌روزرسانی وضعیت بازدید مشتری
    visit_update = update_customer_isvisit(update_data.customer_code)
    edit_update = update_customer_isedit(update_data.customer_code)
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    
    return {
        "message": result.get("message"), 
        "visit": visit_update.get("message")
    }
    
@customer_router.post("/disActiveCustomer")
def disActiveCustomer( disActiveData: DisActiveDescription , username: str = Depends(get_current_user)    ):
    if username is None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        result = sendDisActiveDescription(disActiveData , username)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    visit_update = update_customer_isvisit(disActiveData.customer_code)
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    return {"message": result.get("message"), "visit": visit_update.get("message")}
        

@customer_router.post("/ProductCategory")
def ProductCategoryCustomer( data: ProductCategory , username: str = Depends(get_current_user)    ):
    if username is None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        result = sendProductCategory(data , username)  # ← پارامتر تصحیح شد
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    visit_update = update_customer_isvisit(data.customer_code)
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    return {"message": result.get("message"), "visit": visit_update.get("message")}
        

@customer_router.post("/CRMCustomerDescription")
def crmCustomerDescription ( data: CRMCustomerDescription , username: str = Depends(get_current_user)    ):
    if username is None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        result = sendCRMCustomerDescription(data , username)  # ← پارامتر تصحیح شد
    visit_update = update_customer_isvisit(data.customer_code)
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result



@customer_router.post("/task_complete")
def task_complete ( data: TaskComplete , username: str = Depends(get_current_user)    ):
    if username is None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        visit_update = update_customer_isvisit(data.customer_code,1)
    if "error" in visit_update:
        raise HTTPException(status_code=400, detail=visit_update["error"])
    return visit_update

