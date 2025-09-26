from ..models.base import *
from sqlalchemy import text
import jdatetime
from datetime import datetime
from app.schemas.post_schemas import Point

def save_point(data: Point, username: str):
    with engine.connect() as conn:
        try:
            date_miladi = datetime.now()
            date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
            
            sql = text("""
                INSERT INTO Point_tbl (
                    customer_code, lat , lng , username, date_shamsi, date_miladi

                ) VALUES (
                    :customer_code, :lat, :lng,
                    :username, :date_shamsi, :date_miladi
                )
            """)
            
            conn.execute(sql, {
                "customer_code": data.customer_code,
                "lat": data.lat,
                "lng": data.lng,
                "username": username,
                "date_shamsi": date_shamsi,
                "date_miladi": date_miladi
            })
            
            conn.commit()
            return {"message": "Point saved successfully"}
            
        except Exception as e:
            print(f"Database error in save_point: {e}")
            return {"error": f"Failed to save point: {str(e)}"}
        
   