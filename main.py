from fastapi import FastAPI
from app.routes.auth_router import auth_router
from app.routes.user_route import  user_router
from app.routes.Customer import  customer_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(customer_router)
