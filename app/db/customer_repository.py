import pandas as pd
from sqlalchemy import text
import jdatetime
from datetime import datetime

from app.models.post_model import DisActiveDescription , ProductCategory, CRMCustomerDescription, CustomerEditModel
from ..models.db_model import *

def getCustomerInfo(user):
    try:
        with engine.connect() as conn:
            query = text("""
            SELECT
                کد_مشتری AS customer_code,
                نام_مشتری as customer_name,
                تابلو_مشستری AS customer_board,
                کد_ملی AS national_code,
                محدوده AS "area",
                ناحیه AS "zone",
                مسیر AS "route",
                Latitude AS latitude,
                Longitude AS longitude,
                وضعیت AS status,
                آدرس_مشتری AS address,
                تلفن_اول AS phone,
                تلفن_همراه AS mobile,
                کد_پستی_مشتری AS postal_code,
                u.username AS username,
                v.`visit_Date` as datavisit,
                v.user_idit_data as upload_date,
                v.visit_status as visited,
                v.edit_status as edit
            FROM visit_reports as v 
            join customer as c on v.customer_id = c.کد_مشتری
            join user_tbl as u on u.id = v.user_id
            WHERE v.`visit_Date` = (
                SELECT MAX(v.`visit_Date`) 
                FROM customer
            ) AND u.username = :username
            """)
            
            result = conn.execute(query, {"username": user})
            
            # تبدیل نتیجه به لیست دیکشنری‌ها
            records = []
            for row in result:
                record = {}
                for column, value in row._mapping.items():
                    # تبدیل None به رشته خالی
                    if value is None:
                        record[column] = " "
                    # تبدیل Timestamp به رشته
                    elif column == 'datavisit' and hasattr(value, 'strftime'):
                        record[column] = value.strftime('%Y-%m-%d')
                    # سایر مقادیر
                    else:
                        record[column] = value
                records.append(record)
                
            return records
            
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
   
   
def sendCRMCustomerDescription(data: CRMCustomerDescription , username: str):
    with engine.connect() as conn:
        date_miladi = datetime.now()
        date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
        
        insert_sql = text("""
            INSERT INTO CRMCustomerDescription (customer_code, description_crm, is_customer_visit, is_owner_in_shop, is_cooperation, username, date_shamsi, date_miladi)
            VALUES (:customer_code, :description_crm, :is_customer_visit, :is_owner_in_shop,:is_cooperation, :username, :date_shamsi, :date_miladi)
        """)
        
        conn.execute(insert_sql, {
            "customer_code": int(data.customer_code),
            "description_crm": data.Description,
            "is_customer_visit": data.is_customer_visit,
            "is_owner_in_shop": data.is_owner_in_shop,
            "is_cooperation":data.is_cooperation,
            "username": username,
            "date_shamsi": date_shamsi,
            "date_miladi": date_miladi
        })
        conn.commit()
        return {"message": "CRM customer description saved successfully"}
        
        
def update_customer_isvisit(customer_code: int , visit :int = 2):
    with engine.connect() as conn:
        try:
            sql = text("""
                        UPDATE visit_reports
                        SET visit_status = :visit  
                        WHERE customer_id = :customer_code
            """)
            result = conn.execute(sql, {"customer_code": int(customer_code) , "visit" : visit })
            conn.commit()
            if result.rowcount == 0:
                return {"error": "Customer not found."}
            return {"message": f"isvisit updated to {visit}"}
        except Exception as e:
            return {"error": str(e)}
        
def save_customer_edit(data: CustomerEditModel, username: str):
    with engine.connect() as conn:
        try:
            date_miladi = datetime.now()
            date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
            
            sql = text("""
                INSERT INTO CustomerIditTabel (
                    customer_code, national_code, role_code, postal_code, 
                    customer_board, customer_name, address, mobile_number, 
                    mobile_number2, phone_number, store_area, username, 
                    date_shamsi, date_miladi
                ) VALUES (
                    :customer_code, :national_code, :role_code, :postal_code,
                    :customer_board, :customer_name, :address, :mobile_number,
                    :mobile_number2, :phone_number, :store_area, :username,
                    :date_shamsi, :date_miladi
                )
            """)
            conn.execute(sql, {
                "customer_code": data.customer_code,
                "national_code": data.nationalCode,
                "role_code": data.roleCode,
                "postal_code": data.postalCode,
                "customer_board": data.customerboard,
                "customer_name": data.custumername,
                "address": data.address,
                "mobile_number": data.mobileNumber,
                "mobile_number2": data.mobileNumber2,
                "phone_number": data.phoneNumber,
                "store_area": data.storeArea,
                "username": username,
                "date_shamsi": date_shamsi,
                "date_miladi": date_miladi
            })
            
            conn.commit()
            return {"message": "Customer edit saved successfully"}
            
        except Exception as e:
            print(f"Database error in save_customer_edit: {e}")
            return {"error": f"Failed to save customer edit: {str(e)}"}
        
        
def update_customer_isedit(customer_code: int  , edit:int = 1):
    with engine.connect() as conn:
        try:
            sql = text("""
                        UPDATE visit_reports
                        SET edit_status =:edit
                        WHERE customer_id = :customer_code
            """)
            result = conn.execute(sql, {"customer_code": int(customer_code) , "edit" : edit})
            conn.commit()
            if result.rowcount == 0:
                return {"error": "Customer not found."}
            return {"message": f"isedit updated to {edit}"}
        except Exception as e:
            return {"error": str(e)}
             