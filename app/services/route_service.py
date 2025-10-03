from sqlalchemy import func
from ..models.base import  SessionLocal
from ..models.customer_model import CustomerModel
from ..models.customer_analysis.visit_report import VisitReport
from ..models.user_model import UserModel

def get_routes(): 
     db = None
     try:
          db = SessionLocal()
          routes_query = (db.query(
                                   CustomerModel.مسیر.label("route_id"),
                                   func.count(CustomerModel.کد_مشتری).label("customer_count"))
                          .group_by(CustomerModel.مسیر)
                          .order_by(CustomerModel.مسیر).all())
          routes = [route.route_id for route in routes_query]
          return routes
     except Exception as e:
          print(f"خطا در دریافت مسیرها: {str(e)}")
          return {"error": str(e) , 'success':False}
     finally:
          if db is not None:
               db.close()
               
def add_user_route(route_id , username , datetime_val):
     db = None
     try:
          db = SessionLocal()
          user = db.query(UserModel).filter(UserModel.username == username).first()
          if not user:
               return {"error": "کاربر یافت نشد", 'success': False}
          customers = db.query(CustomerModel).filter(CustomerModel.مسیر == route_id).all()
          if not customers:
               return {"error": "هیچ مشتری در این مسیر یافت نشد", 'success': False}
          
          for customer in  customers:
               visit_reports = VisitReport(customer_id= customer.کد_مشتری,
                                           user_id= user.id ,
                                           visit_Date =datetime_val )
               db.add(visit_reports)  
          db.commit()  
          return {"success": True}
     except Exception as e:
          print(f"خطا در افزودن مسیر: {str(e)}")
          return {"error": str(e) , 'success':False}
     finally:
          if db is not None:
               db.close()
