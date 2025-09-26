from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy import null
from app.auth.auth_handler import get_current_user
from app.schemas.response_schemas import UserModel
from app.services.user_service import getUserDB , saveUserDB
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user_schemas import User

user_router = APIRouter()


@user_router.get("/getUserdata", response_model=UserModel)
def get_user_data(username: str = Depends(get_current_user)):
    user = getUserDB(username)
    return user


#TODO باید کاری کنم که فقط افرادی که دسترسی میدم بتونند یوزر تعریف کنن
@user_router.post("/register")
def register_user(data: User, username: str = Depends(get_current_user)):
    if username is not null :
        result = saveUserDB(data)
        return result
    else :
        raise HTTPException(status_code=400, detail=visit_update["error"])
        
