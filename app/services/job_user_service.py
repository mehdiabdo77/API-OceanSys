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

def set_job_user(user_id):
    db = None
    try:
        db = SessionLocal()

        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "data": {}}
    finally:
        if db is not None:
            db.close()