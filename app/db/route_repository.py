from unittest import result
from sqlalchemy import text
from datetime import datetime
from ..models.db_model import engine

def get_routes(): 
     try:
          with engine.connect() as conn:
               query= text("""
                              SELECT DISTINCT مسیر as route_id, COUNT(کد_مشتری) as customer_count
                              FROM customer
                              GROUP BY مسیر
                              ORDER BY مسیر
                         """)
               result = conn.execute(query)
               print(result)
               routes =[]
               for row in result:
                    routes.append(row.route_id,)
               return routes
     except Exception as e:
          print(f"خطا در دریافت مسیرها: {str(e)}")
          return {"error": str(e) , 'success':False}

def add_user_route(route_id , username , datetime):
     try:
          with engine.connect() as conn:
               query = text("""
                            INSERT INTO visit_reports (customer_id, user_id, visit_Date)
                              SELECT c.کد_مشتری, u.id, :datetime
                              FROM customer c
                              CROSS JOIN user_tbl u
                              WHERE c.مسیر = :route_id
                              AND u.username = :username;
                            """)
               conn.execute(query,{"route_id":route_id , "username":username , "datetime":datetime})
               return {"success": True}
     except Exception as e:
          print(f"خطا در افزودن مسیر: {str(e)}")
          return {"error": str(e) , 'success':False}
