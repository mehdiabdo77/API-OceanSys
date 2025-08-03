def verify_password(plain_password: str, hashed_password: str):
    return plain_password == str(hashed_password)
