from cProfile import label
from unittest import result
from sqlalchemy import text
from datetime import datetime
from ..models.base import  SessionLocal , relationship
from ..models.customer_model import Customer
from ..models.visit_report import VisitReport
from ..models.user_model import User




def get_routes(): 
     try:
          db = SessionLocal()
          routes_query = (db.query(Customer.مسیر.label("route_id"),
                                   func.count(Customer.کد_مشتری),
                                   label("customer_count"))
                          .group_by(Customer.مسیر)
                          .order_by(Customer.مسیر).all())
          routes = [route.route_id for route in routes_query]
          return routes
     except Exception as e:
          print(f"خطا در دریافت مسیرها: {str(e)}")
          return {"error": str(e) , 'success':False}
     finally:
          db.close()

# TODO لتفا محدوده هم بهش اضافه کن 
def add_user_route(route_id , username , datetime_val):
     try:
          db = SessionLocal()
          user = db.query(User).filter(User.username == username).first()
          if not user:
               return {"error": "کاربر یافت نشد", 'success': False}
          customers = db.query(Customer).filter(Customer.مسیر == route_id).all()
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
          db.close()
