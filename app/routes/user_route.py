from fastapi import APIRouter, Depends
from app.auth.auth_handler import get_current_user
from app.models.response_model import UserModel
from app.db.user_repository import getUserDB
from app.utils.password import verify_password
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

user_router = APIRouter()


@user_router.get("/getUserdata", response_model=UserModel)
def get_user_data(username: str = Depends(get_current_user)):
    user = getUserDB(username)
    return user
