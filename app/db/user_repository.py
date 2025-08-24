import pandas as pd
from sqlalchemy import text
import jdatetime
from datetime import datetime
from ..models.db_model import *


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

