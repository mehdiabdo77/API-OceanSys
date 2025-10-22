from ctypes import Union
from shelve import DbfilenameShelf
from typing import Optional
import pandas as pd
from sqlalchemy import text, true
import jdatetime

from app.services.permission_service import get_all_permission_user
from ..core.base import *
from app.schemas.user_schemas import User
from app.models.user.user_model import UserModel
from app.utils.security import hash_password

def getUserDB(
     user: Optional[int | str]
):
     db = None
     try:
          db = SessionLocal()
          if isinstance(user, int):
               query_result = db.query(UserModel).filter(UserModel.id == user).first()
          else:
               query_result = db.query(UserModel).filter(UserModel.username == user).first()
          print(f"Query result: {query_result}")
          if query_result:
               id_user = query_result.id
               data = {
                    "id" : id_user,
                     "username": query_result.username,
                     "first_name": query_result.first_name,
                     "last_name": query_result.last_name,
                     "password_hash": query_result.password_hash,
                     "is_active": query_result.is_active,
                     "permission": get_all_permission_user(id_user),
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

def getAllUsersDB(
     user: Optional[int | str]
):
     db = None
     try:
          db = SessionLocal()
          query_result = db.query(UserModel).all()
          users_list = []

          print(f"Query result: {query_result}")
          if query_result:
               id_user = query_result.id
               data = {
                    "id" : id_user,
                     "username": query_result.username,
                     "first_name": query_result.first_name,
                     "last_name": query_result.last_name,
                     "password_hash": query_result.password_hash,
                     "is_active": query_result.is_active,
                     "permission": get_all_permission_user(id_user),
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
               
               
def getAllUsersDB():
     db = None
     try:
          db = SessionLocal()
          query_result = db.query(UserModel).all()
          users_list = []
          
          for user in query_result:
               user_data = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "password_hash": user.password_hash,
                    "is_active": user.is_active,
                    "permission": get_all_permission_user(user.id),
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
               }
               users_list.append(user_data)
               
          return users_list
     except Exception as e:
          print(f"Error in getAllUsersDB: {str(e)}")
          return []
     finally:
          if db is not None:
               db.close()