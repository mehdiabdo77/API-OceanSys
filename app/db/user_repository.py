import pandas as pd
from sqlalchemy import text
import jdatetime
from datetime import datetime
from ..models.db_model import *


# TODO باید از دیتا بیس بخونه و هش هم بکنه
def getUserDB(
     user
):
     try:
          df = pd.read_excel("db.xlsx")
          row = df[df['user'] == user ].iloc[0]
          row = row.to_dict()
          return  row
     except:
          return None
