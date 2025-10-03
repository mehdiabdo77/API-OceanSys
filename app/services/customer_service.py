from sqlalchemy import desc, func, text
import jdatetime
from datetime import datetime
from app.models.customer_analysis.CRM_customer_description import CRMCustomerDescriptionModel
from app.models.customer_model import CustomerModel
from app.models.customer_analysis.disactive_description_model import DisActiveDescriptionModel
from app.models.customer_analysis.Customer_Idit import CustomerIditModel
from app.models.customer_analysis.product_category_customer import ProductCategoryCustomerModel
from app.models.user_model import UserModel
from app.models.customer_analysis.visit_report import VisitReportModel
from app.schemas.customer_schemas import CustomerEdit, DisActiveDescription , ProductCategory, CRMCustomerDescription
from ..models.base import SessionLocal, engine

def getCustomerInfo(user):
    db = None
    try:
        db = SessionLocal()
        subquery = db.query(func.max(VisitReportModel.visit_Date)).scalar()
        query = (
            db.query(
                CustomerModel.کد_مشتری.label("customer_code"),
                CustomerModel.نام_مشتری.label("customer_name"),
                CustomerModel.تابلو_مشستری.label("customer_board"),
                CustomerModel.کد_ملی.label("national_code"),
                CustomerModel.محدوده.label("area"),
                CustomerModel.ناحیه.label("zone"),
                CustomerModel.مسیر.label("route"),
                CustomerModel.Latitude.label("latitude"),
                CustomerModel.Longitude.label("longitude"),
                CustomerModel.وضعیت.label("status"),
                CustomerModel.آدرس_مشتری.label("address"),
                CustomerModel.تلفن_اول.label("phone"),
                CustomerModel.تلفن_همراه.label("mobile"),
                CustomerModel.کد_پستی_مشتری.label("postal_code"),
                UserModel.username.label("username"),
                VisitReportModel.visit_Date.label("datavisit"),
                VisitReportModel.user_idit_data.label("upload_date"),
                VisitReportModel.visit_status.label("visited"),
                VisitReportModel.edit_status.label("edit")
            ).join(VisitReportModel , VisitReportModel.customer_id== CustomerModel.کد_مشتری))\
                .join(UserModel , UserModel.id == VisitReportModel.user_id)\
                .filter(VisitReportModel.visit_Date == subquery)\
                .filter(UserModel.username == user)
        result = query.all() 

            # تبدیل نتیجه به لیست دیکشنری‌ها
        records = []
        for row in result:
            record = {}
            for key in row._fields:
                value = getattr(row , key)
                if value is None :
                    record[key] = " "
                elif key == 'datavisit' and hasattr(value, 'strftime'):
                    record[key] = value.strftime('%Y-%m-%d')
                else :
                    record[key] = value
            records.append(record)
        return records        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()

def sendDisActiveDescription(data: DisActiveDescription , username: str):
    db = None
    user_id = None
    try:
        db = SessionLocal()
        count = db.query(func.count(DisActiveDescriptionModel.customer_code))\
            .filter(DisActiveDescriptionModel.customer_code == data.customer_code).scalar()
        print(count)
        if int(count) > 0:
            return {"error": "This customer has already been deactivated."}
        user_data = db.query(UserModel).filter(UserModel.username == username ).first()
        if user_data:
            user_id = user_data.id
        disActive_record = DisActiveDescriptionModel(
        customer_code = int(data.customer_code),
        Reason = data.Reason,
        Description = data.Description,
        user_id = user_id,
        created_at =  datetime.now()
            )
        print(disActive_record)
        db.add(disActive_record)
        db.commit()
        return {"message": "Customer deactivated successfully"}
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()
    
    
 
def sendProductCategory(data: ProductCategory , username: str):
    db = None
    user_id = None
    try:
        db = SessionLocal()
        user_data = db.query(UserModel).filter(UserModel.username == username ).first()
        if user_data:
            user_id = user_data.id
        for item in data.sku:
            product_category_record = ProductCategoryCustomerModel(
            customer_code = int(data.customer_code),
            sku = item,
            user_id = user_id,
            created_at =  datetime.now()
                )
            db.add(product_category_record)
            db.commit()
            
        

        return {"message": "Product categories saved successfully"}
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()
   
   
def sendCRMCustomerDescription(data: CRMCustomerDescription , username: str):
    db = None
    user_id = None
    try:
        db = SessionLocal()
        user_data = db.query(UserModel).filter(UserModel.username == username ).first()
        if user_data:
            user_id = user_data.id
        crm_record = CRMCustomerDescriptionModel(
            crm_record = CRMCustomerDescriptionModel(
                customer_code=int(data.customer_code),
                description_crm=data.Description,       
                is_customer_visit=data.is_customer_visit,
                is_owner_in_shop=data.is_owner_in_shop,
                is_cooperation=data.is_cooperation,
                user_id=user_id,                       
                created_at=datetime.now()             
                 )
                )
        db.add(crm_record)
        db.commit()  
        return {"message": "CRM customer description saved successfully"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()
        
def save_customer_edit(data: CustomerEdit, username: str):
    db = None
    user_id = None
    try:
        db = SessionLocal()
        user_data = db.query(UserModel).filter(UserModel.username == username ).first()
        if user_data:
            user_id = user_data.id
        customer_record = CustomerIditModel(
            customer_code = data.customer_code,
            national_code = data.nationalCode,
            role_code = data.roleCode,
            postal_code = data.postalCode,
            customer_board = data.customerboard,
            customer_name = data.custumername,
            address = data.address,
            mobile_number = data.mobileNumber,
            mobile_number2 = data.mobileNumber2,
            phone_number = data.phoneNumber,
            store_area = data.storeArea,
            user_id = user_id,
            created_at = datetime.now()  
        )
        db.add(customer_record)
        db.commit()
        return {"message": "CRM customer description saved successfully"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()
        
def update_customer_isvisit(customer_code: int , visit :int = 2):
    db = None
    try:
        db = SessionLocal()
        report =  db.query(VisitReportModel)\
           .filter(VisitReportModel.customer_id == customer_code)\
           .order_by(desc(VisitReportModel.id))\
           .first()
        if report:
            report.visit_status = visit # type: ignore
        db.commit()       
        db.refresh(report) 

        
        db.commit()
        return {"message": "CRM customer description saved successfully"}
    except Exception as e:
        if db is not None:
            db.rollback()
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()
             

def update_customer_isedit(customer_code: int, edit: int = 1):
    db = None
    try:
        db = SessionLocal()
        report = db.query(VisitReportModel)\
                   .filter(VisitReportModel.customer_id == customer_code)\
                   .order_by(VisitReportModel.id.desc())\
                   .first()

        if not report:
            return {"error": "Customer not found."}

        report.edit_status = bool(edit)  # type: ignore
        db.commit()
        db.refresh(report)

        return {"message": f"isedit updated to {edit}"}

    except Exception as e:
        if db is not None:
            db.rollback()
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()