from app.models.point_model import PointModel
from ..core.base import SessionLocal, engine
import jdatetime
from datetime import datetime
from app.schemas.post_schemas import Point

def save_point(data: Point, username: str):
    db = None
    try:
        db = SessionLocal()
        date_miladi = datetime.now()
        date_shamsi = jdatetime.datetime.now().strftime('%Y/%m/%d')
            
        point_record  = PointModel(
            customer_code = data.customer_code,
            lat = data.lat,
            lng = data.lng,
            username = username,
            date_shamsi = date_shamsi,
            date_miladi = date_miladi
            )
        db.add(point_record)
            
        return {"message": "Point saved successfully"}
            
    except Exception as e:
        print(f"Database error in save_point: {e}")
        return {"error": f"Failed to save point: {str(e)}"}
    finally:
        if db is not None:
            db.close()
        
   