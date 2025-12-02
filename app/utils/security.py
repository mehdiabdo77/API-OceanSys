from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__memory_cost=65536,
    argon2__time_cost=3,
    argon2__parallelism=4,
)

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
