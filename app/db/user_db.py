import pandas as pd
from ..models.db_model import *

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
     
def getCustomerInfo(
     user
):   

    try:
        # خواندن فایل اکسل
        df = pd.read_sql(query, engine)
        
        df = df[df['username'] == user ]
        
        # تبدیل NaN/None به مقدار قابل قبول برای JSON
        cleaned_df = df.where(pd.notnull(df), " ")
        
        # تبدیل به دیکشنری
        result = cleaned_df.to_dict("records")
        
        print("Data loaded successfully:", result)
        return result
        
    except FileNotFoundError:
        print("Error: File 'coustumer.xlsx' not found")
        return {"error": "File not found", "data": {}}
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}