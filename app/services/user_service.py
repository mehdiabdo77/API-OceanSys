from ctypes import Union
from shelve import DbfilenameShelf
from typing import Optional
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

from app.models.user.role_model import RoleModel # اضافه شد برای جستجوی نام نقش

def saveUserDB(
     dataUser : User,
     role_name : Optional[str] = None
):
     db = None
     password_hash = hash_password(dataUser.password)
     try:
          db = SessionLocal()
          
          # استفاده از نام نقش برای پیدا کردن آیدی
          final_role_name = role_name if role_name is not None else (dataUser.role.value if dataUser.role else None)
          
          if final_role_name is None:
               return {"message": "Role is required"}
          
          # بررسی تکراری بودن نام کاربری
          existing_user = db.query(UserModel).filter(UserModel.username == dataUser.username).first()
          if existing_user:
               return {"message": "username_already_exists"}
               
          role_record = db.query(RoleModel).filter(RoleModel.name == final_role_name.upper()).first()
          if not role_record:
               return {"message": f"Role {final_role_name} not found"}
          
          user_record = UserModel(
               username = dataUser.username,
               first_name = dataUser.first_name,
               last_name = dataUser.last_name,
               password_hash = password_hash,
               is_active = True,
               role_id = role_record.id
               )
          db.add(user_record)
          db.commit()
          db.refresh(user_record)
          
          return {"message": "successfully", "user_id": user_record.id}
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
               
               
def set_user_status(username: str, is_active: bool):
     db = None
     try:
          db = SessionLocal()
          user = db.query(UserModel).filter(UserModel.username == username).first()
          if not user:
               return {"message": "User not found"}
          
          user.is_active = is_active
          db.commit()
          return {"message": "successfully"}
     except Exception as e:
          if db:
               db.rollback()
          print(f"Error in set_user_status: {str(e)}")
          return {"message": "Error updating user status"}
     finally:
          if db:
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