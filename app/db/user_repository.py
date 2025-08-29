import pandas as pd
from sqlalchemy import text
import jdatetime
from datetime import datetime
from ..models.db_model import *
from app.models.post_model import User
from app.utils.password import hash_password



# TODO باید از دیتا بیس بخونه و هش هم بکنه
def getUserDB(
     user: str
):
     with engine.connect() as conn:
          try:
               sql = text(
                    """
                         SELECT * from user_tbl WHERE username = :username
                    """
               )
               result = conn.execute(sql, {"username": user})
               row = result.mappings().fetchone()
               if not row:
                    return None
               data = dict(row)
               return data
          except Exception:
               return None

def saveUserDB(
     dataUser : User
):
     date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
     password_hash = hash_password(dataUser.password)
     with engine.connect() as conn:
          try:
               sql = text("""
                    INSERT INTO user_tbl (username, full_name, password_hash, department_id, position_id, created_at_jalali, updated_at_jalali)
                    VALUES (:username, :full_name, :password_hash, :department_id, :position_id, :date_shamsi, :date_shamsi)
               """)
               conn.execute(sql, {
                    "username": dataUser.username,
                    "full_name": dataUser.fullName,
                    "password_hash": password_hash,
                    "department_id": dataUser.departmentID,
                    "position_id": dataUser.positionID,
                    "date_shamsi": date_shamsi
               })
               conn.commit()
               return {"message": "User saved successfully"}
          except Exception:
               return {"message": "User saved unsuccessfully"}
