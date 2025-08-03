from typing import List
from fastapi import APIRouter, Depends
from app.auth.auth_handler import get_current_user
from app.db.user_db import getCustomerInfo
from app.models.response_model import CustomerModel
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.post_model import CustomerEditModel


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