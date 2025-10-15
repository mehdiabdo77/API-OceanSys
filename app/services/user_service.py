from shelve import DbfilenameShelf
import pandas as pd
from sqlalchemy import text, true
import jdatetime
from ..core.base import *
from app.schemas.user_schemas import User
from app.models.user.user_model import UserModel
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
                    "id" : query_result.id,
                     "username": query_result.username,
                     "first_name": query_result.first_name,
                     "last_name": query_result.last_name,
                     "password_hash": query_result.password_hash,
                     "is_active": query_result.is_active,
                     "role_id": query_result.role_id,
                     "created_at": query_result.created_at,
                     "updated_at": query_result.updated_at,
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
     password_hash = hash_password(dataUser.password)
     try:
          db = SessionLocal()
          user_record = UserModel(
               username = dataUser.username,
               first_name = dataUser.first_name,
               last_name = dataUser.last_name,
               password_hash = password_hash,
               is_active = True,
               role_id = dataUser.role_id
               )
          db.add(user_record)
          db.commit()
          return {"message": "successfully"}
     except Exception as e:
          if db is not None:
              db.rollback()
          print(f"Error saving user: {e}")
          return {"message": "User saved unsuccessfully"}
     finally:
          if db is not None:
               db.close()
               
               
def Countuser():
     db = None
     try:
          db = SessionLocal()
          query_result = db.query(UserModel).count()
          print(query_result)
          return query_result
     except Exception as e:
        print(f"Error counting users: {e}")
     finally:
          if db is not None:
               db.close()