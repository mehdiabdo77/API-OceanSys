from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    هش کردن پسورد 
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    بررسی صحت پسورد وارد شده
    """
    return pwd_context.verify(plain_password, hashed_password)
