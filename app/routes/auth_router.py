from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from app.auth.auth_handler import create_access_token, decode_token
from app.models.response_model import UserModel
from app.db.user_repository import getUserDB
from app.utils.password import verify_password
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter()

@auth_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = getUserDB(form_data.username)
    if not user or not verify_password(form_data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user['username']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}