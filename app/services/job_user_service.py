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
from app.schemas.customer_schemas import CustomerEdit, DisActiveDescription , ProductCategory, CRMCustomerDescription, JobUserRequest
from ..core.base import SessionLocal, engine

def set_job_user(data: JobUserRequest, user_id: int):
    db = None
    try:
        db = SessionLocal()
        
        # پیدا کردن کاربر بر اساس ID از توکن
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return {"error": "User not found", "success": False}
        
        # پیدا کردن مشتریان بر اساس فیلترهای ارسالی
        customers = db.query(CustomerModel).filter(
            CustomerModel.route == data.route,
            CustomerModel.area == data.area,
            CustomerModel.region == data.region
        ).all()
        
        if not customers:
            return {"error": "No customers found for the given criteria", "success": False}
        
        # تبدیل تاریخ شمسی یا میلادی به فرمت مناسب (در اینجا فرض بر این است که تاریخ به صورت رشته ارسال می‌شود)
        # اگر نیاز به تبدیل خاصی است می‌توان از jdatetime استفاده کرد
        
        visit_date_obj = None
        try:
            visit_date_obj = datetime.strptime(data.visit_date, '%Y-%m-%d')
        except ValueError:
            # TODO  اگر فرمت دیگری مد نظر است یا تاریخ شمسی است، اینجا مدیریت شود 
            pass

        new_reports = []
        for customer in customers:
            report = VisitReportModel(
                customer_id=customer.customer_code,
                user_id=user.id,
                edit_status=False,
                visit_Date=visit_date_obj if visit_date_obj else data.visit_date
            )
            db.add(report)
            new_reports.append(report)
            
        db.commit()
        return {"message": f"Successfully assigned {len(new_reports)} customers to user {user.username}", "success": True}
        
    except Exception as e:
        if db:
            db.rollback()
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "success": False}
    finally:
        if db is not None:
            db.close()


