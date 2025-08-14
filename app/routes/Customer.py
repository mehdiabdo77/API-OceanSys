from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from app.auth.auth_handler import get_current_user
from app.db.customer_repository import getCustomerInfo, sendDisActiveDescription , sendProductCategory
from app.models.response_model import CustomerModel
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.post_model import CustomerEditModel, DisActiveDescription, ProductCategory


customer_router = APIRouter()


@customer_router.get(
    "/getCustomerData",
    response_model=List[CustomerModel] 
    )
def get_customer_data(username: str = Depends(get_current_user) , ):
    customerInfo = getCustomerInfo(username)
    return customerInfo




@customer_router.post("/editcoustomerinfo")
def editCustomerData( update_data: CustomerEditModel  , username: str = Depends(get_current_user)    ):
    if username == None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        pass
    
    
@customer_router.post("/disActiveCustomer")
def disActiveCustomer( disActiveData: DisActiveDescription , username: str = Depends(get_current_user)    ):
    if username is None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        result = sendDisActiveDescription(disActiveData , username)
    print(result)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
        

@customer_router.post("/ProductCategory")
def productCategory( data: ProductCategory , username: str = Depends(get_current_user)    ):
    if username is None :
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        result = sendProductCategory(data , username)  # ← پارامتر تصحیح شد
    print(result)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result     

#detectProductCategoryIntent
