from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.utils.security import verify_password
from app.services.user_service import getUserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=30))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise ValueError("Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def authenticate_user(username: str, password: str):
    '''
    بررسی صحت این که یوزر که کاربر داده توی دیتا بیس هست
    در صورت وجود نداشتن مقدار None بر میگرداند.
    '''
    user = getUserDB(username)
    if not user or not verify_password(password, user['password']):
        return None
    return user

#
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
    ورود کاربر با ارسال یوزر و پسورد
    دریافت توکن در صورت صحت اطلاعات
    '''
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user['user']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# گرفتن اطلاعات تکمیلی یوزر  که وارد صفحه شده
def get_current_user(token: str = Depends(oauth2_scheme)):
    '''
    استخراج نام کاربر از طرق توکن ارسالی کاربر 
    عملیات دی کد کردن از طریق تابع decode_token انجام میشود
    '''
    try:
        username = decode_token(token)
        print(username)
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")





