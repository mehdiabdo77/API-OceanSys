from sqlalchemy import desc, func, text
import jdatetime
from datetime import datetime
from app.models.scanner.CRM_customer_description import CRMCustomerDescriptionModel
from app.models.customer_model import CustomerModel
from app.models.scanner.disactive_description_model import DisActiveDescriptionModel
from app.models.scanner.Customer_Idit import CustomerIditModel
from app.models.scanner.product_category_customer import ProductCategoryCustomerModel
from app.models.user.user_model import UserModel
from app.models.scanner.visit_report import VisitReportModel
from app.schemas.customer_schemas import CustomerEdit, DisActiveDescription , ProductCategory, CRMCustomerDescription, JobUserRequest
from ..core.base import SessionLocal, engine

def set_job_user(data: JobUserRequest):
    db = None
    try:
        db = SessionLocal()
        
        # پیدا کردن کاربر بر اساس ID از توکن
        user = db.query(UserModel).filter(UserModel.id == data.userId).first()
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



def del_job_user(data: JobUserRequest):
    db = None
    try:
        db = SessionLocal()

        user = db.query(UserModel).filter(UserModel.id == data.userId).first()
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

        customer_ids = [c.customer_code for c in customers]

        # پیدا کردن گزارش‌های تخصیص‌یافته به این کاربر که هنوز ویزیت نشده‌اند
        reports_query = db.query(VisitReportModel).filter(
            VisitReportModel.customer_id.in_(customer_ids),
            VisitReportModel.user_id == data.userId,
            VisitReportModel.edit_status == False
        )

        reports = reports_query.all()

        if not reports:
            return {"error": "No unassigned/pending visit reports found to delete", "success": False}

        deleted_count = reports_query.delete(synchronize_session=False)
        db.commit()

        return {
            "message": f"Successfully deleted {deleted_count} visit report(s) for user {user.username}",
            "success": True
        }

    except Exception as e:
        if db:
            db.rollback()
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e), "success": False}
    finally:
        if db is not None:
            db.close()

# {
#   "route": "104",
#   "area": "04",
#   "region": "41",
#   "visit_date": "2024-01-16"
# }