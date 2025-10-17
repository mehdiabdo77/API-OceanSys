from sqlalchemy import desc, func, text
import jdatetime
from datetime import datetime
from app.models.customer_analysis.CRM_customer_description import CRMCustomerDescriptionModel
from app.models.customer_model import CustomerModel
from app.models.customer_analysis.disactive_description_model import DisActiveDescriptionModel
from app.models.customer_analysis.Customer_Idit import CustomerIditModel
from app.models.customer_analysis.product_category_customer import ProductCategoryCustomerModel
from app.models.user.user_model import UserModel
from app.models.customer_analysis.visit_report import VisitReportModel
from app.schemas.customer_schemas import CustomerEdit, DisActiveDescription , ProductCategory, CRMCustomerDescription
from ..core.base import SessionLocal, engine

def getCustomerInfo(user_id):
    db = None
    try:
        db = SessionLocal()
        subquery = db.query(func.max(VisitReportModel.visit_Date)).scalar()
        query = (
            db.query(
                CustomerModel.customer_code,
                CustomerModel.customer_name,
                CustomerModel.customer_board,
                CustomerModel.national_code,
                CustomerModel.area,
                CustomerModel.zone,
                CustomerModel.route,
                CustomerModel.latitude,
                CustomerModel.longitude,
                CustomerModel.status,
                CustomerModel.address,
                CustomerModel.phone,
                CustomerModel.mobile,
                CustomerModel.mobile2,
                CustomerModel.postal_code,
            )
            .join(VisitReportModel, VisitReportModel.customer_id == CustomerModel.customer_code)
            .join(UserModel, UserModel.id == VisitReportModel.user_id)
            .filter(VisitReportModel.visit_Date == subquery)
            .filter(UserModel.id == user_id)
        )
        result = query.all()

        records = []
        for row in result:
            data = dict(row._mapping)
            for key, value in list(data.items()):
                if key in ("latitude", "longitude") and value is not None:
                    try:
                        data[key] = float(value)
                    except Exception:
                        data[key] = str(value)
                elif value is None:
                    data[key] = " "
            records.append(data)
        return records
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()

def sendDisActiveDescription(data: DisActiveDescription , user_id: int):
    db = None
    try:
        db = SessionLocal()
        count = db.query(func.count(DisActiveDescriptionModel.customer_code))\
            .filter(DisActiveDescriptionModel.customer_code == data.customer_code).scalar()
        print(count)
        if int(count) > 0:
            return {"error": "This customer has already been deactivated."}
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
    
    
 
def sendProductCategory(data: ProductCategory , user_id: int):
    db = None
    try:
        db = SessionLocal()
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
   
   
def sendCRMCustomerDescription(data: CRMCustomerDescription , user_id: int):
    db = None
    try:
        db = SessionLocal()
        crm_record = CRMCustomerDescriptionModel(
                customer_code=int(data.customer_code),
                description_crm=data.Description,       
                is_customer_visit=data.is_customer_visit,
                is_owner_in_shop=data.is_owner_in_shop,
                is_cooperation=data.is_cooperation,
                user_id=user_id,                       
                created_at=datetime.now()             
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
        
def save_customer_edit(data: CustomerEdit, user_id: int):
    db = None
    try:
        db = SessionLocal()
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