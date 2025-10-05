from shelve import DbfilenameShelf
import pandas as pd
from sqlalchemy import text, true
import jdatetime
from ..core.base import *
from app.schemas.user_schemas import User
from app.models.user_model import UserModel
from app.utils.security import hash_password

def getUserDB(
     user: str
):
     db = None
     try:
          db = SessionLocal()
          query_result = db.query(UserModel).filter(UserModel.username == user).first()
          print(f"Query result: {query_result}")
          if query_result:
               data = {
                     "username": query_result.username,
                     "first_name": query_result.first_name,
                     "last_name": query_result.last_name,
                     "password_hash": query_result.password_hash,
                     "is_active": query_result.is_active,
                     "department_id": query_result.department_id,
                     "position_id": query_result.position_id,
                     "created_at": query_result.created_at,
                     "updated_at": query_result.updated_at,
                     "created_at_jalali": query_result.created_at_jalali,
                     "updated_at_jalali": query_result.updated_at_jalali,
               }
               return data
          return None
     except Exception as e:
          print(f"Error in getUserDB: {str(e)}")
          return None
     finally:
          if db is not None:
               db.close()

def saveUserDB(
     dataUser : User
):
     db = None
     date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
     password_hash = hash_password(dataUser.password)
     try:
          db = SessionLocal()
          user_record = UserModel(
               username = dataUser.username,
               full_name = dataUser.fullName,
               password_hash = password_hash,
               is_active = True,
               department_id = dataUser.departmentID,
               position_id = dataUser.positionID,
               created_at_jalali = date_shamsi,
               updated_at_jalali = date_shamsi
               )
          db.add(user_record)
          db.commit()
          return {"message": "User saved successfully"}
     except Exception:
          return {"message": "User saved unsuccessfully"}
     finally:
          if db is not None:
               db.close()