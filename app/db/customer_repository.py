import pandas as pd
from sqlalchemy import text
import jdatetime
from datetime import datetime

from app.models.post_model import DisActiveDescription , ProductCategory
from ..models.db_model import *

def getCustomerInfo(
     user
):   

    try:
        # خواندن فایل اکسل
        df = pd.read_sql(query_customergetinfo, engine)
        
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
   

def sendDisActiveDescription(data: DisActiveDescription , username: str):
    with engine.connect() as conn:
        # بررسی وجود قبلی
        check_sql = text("""
            SELECT COUNT(*) FROM DisActiveDescription WHERE customer_code = :customer_code
        """)
        result = conn.execute(check_sql, {"customer_code": data.customer_code}).scalar()
        print(f"Check result for customer_code {data.customer_code}: {result}")
        if int(result) > 0:
            return {"error": "This customer has already been deactivated."}
        # درج جدید
        date_miladi = datetime.now()
        date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
        sql = text("""
            INSERT INTO DisActiveDescription (customer_code, Reason, Description, username, date_shamsi, date_miladi)
            VALUES (:customer_code, :Reason, :Description, :username, :date_shamsi, :date_miladi)
        """)
        
        conn.execute(sql, {
            "customer_code": int(data.customer_code),
            "Reason": data.Reason,
            "Description": data.Description,
            "username": username,
            "date_shamsi": date_shamsi,
            "date_miladi": date_miladi
            
        })
        conn.commit()
        return {"message": "Customer deactivated successfully"}
    
 
def sendProductCategory(data: ProductCategory , username: str):
    with engine.connect() as conn:
        #TODO بعد کاری کن اخرین رکرود تو اینجا در هر روز زخیره بشه
        date_miladi = datetime.now()
        date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
        
        insert_sql = text("""
            INSERT INTO ProductCategoryCustomer (customer_code, sku, username, date_shamsi, date_miladi)
            VALUES (:customer_code, :sku, :username, :date_shamsi, :date_miladi)
        """)

        for item in data.sku:            # ذخیرهٔ هر SKU در یک ردیف مستقل
            conn.execute(insert_sql, {
                "customer_code": int(data.customer_code),
                "sku": item,
                "username": username,
                "date_shamsi": date_shamsi,
                "date_miladi": date_miladi
            })
        
        conn.commit()
        return {"message": "Product categories saved successfully"}
        