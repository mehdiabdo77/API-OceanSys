from sqlalchemy import create_engine



db_config = {
    'host': '127.0.0.1',  
    'user': 'root',   
    'password': '58003695', 
    'database': 'ocean', 
    'port': 3306        
}


connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"


engine = create_engine(connection_string)


query_customergetinfo = """
SELECT
    کد_مشتری AS customer_code,
    نام_مشتری as customer_name,
    تابلو_مشستری AS customer_board,
    کد_ملی AS national_code,
    محدوده AS "area",
    ناحیه AS "zone",
    مسیر AS "route",
    Latitude AS latitude,
    Longitude AS longitude,
    وضعیت AS status,
    آدرس_مشتری AS address,
    تلفن_اول AS phone,
    تلفن_همراه AS mobile,
    کد_پستی_مشتری AS postal_code,
    'mahdi' AS username,
    "1404/04/05" as datavisit,
    isvisit as visited,
    0 as edit
FROM customer
"""
