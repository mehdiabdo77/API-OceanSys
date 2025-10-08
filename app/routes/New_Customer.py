from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from app.auth.auth_handler import get_current_user
from app.services.customer_service import getCustomerInfo
from app.schemas.customer_schemas import CustomerModel 
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

new_customer_router = APIRouter()


@new_customer_router.get(
    "/getCustomerData",
    response_model=List[CustomerModel] 
    )
def get_customer_data(username: str = Depends(get_current_user) , ):
    """
    ایجاد مشتری جدید
    """
    customerInfo = getCustomerInfo(username)
    return customerInfo


