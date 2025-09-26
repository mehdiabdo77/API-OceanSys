# FastAPI Application

This project is a FastAPI application that provides user authentication and management features. It utilizes JWT for token-based authentication and is structured to separate concerns into different modules.

## Project Structure

```
OceanSys-API
├── app
│   ├── auth
│   │   └── auth_handler.py       # مدیریت احراز هویت و توکن‌ها
│   ├── core
│   │   └── config.py             # تنظیمات اصلی پروژه
│   ├── models                    # مدل‌های SQLAlchemy (ORM)
│   │   ├── base.py               # تنظیمات پایه SQLAlchemy
│   │   ├── customer_model.py     # مدل مشتری
│   │   ├── user_model.py         # مدل کاربر
│   │   └── visit_report.py       # مدل گزارش بازدید
│   ├── routes                    # مسیرهای API
│   │   ├── Customer.py           # مسیرهای مربوط به مشتری
│   │   ├── auth_router.py        # مسیرهای احراز هویت
│   │   ├── point.py              # مسیرهای مربوط به نقاط
│   │   ├── user_route.py         # مسیرهای مربوط به کاربر
│   │   └── visit.py              # مسیرهای مربوط به بازدید
│   ├── schemas                   # طرح‌های Pydantic برای  
│   │   ├── customer_schemas.py   # طرح‌های مربوط به مشتری
│   │   ├── post_schemas.py       # طرح‌های مربوط به پست‌ها
│   │   ├── response_schemas.py   # طرح‌های مربوط به پاسخ‌ها
│   │   └── user_schemas.py       # طرح‌های مربوط به کاربر
│   ├── services                  # منطق تجاری
│   │   ├── customer_service.py   # سرویس مشتری
│   │   ├── point_service.py      # سرویس نقاط
│   │   ├── route_service.py      # سرویس مسیرها
│   │   └── user_service.py       # سرویس کاربر
│   └── utils
│       └── security.py           # توابع امنیتی
├── main.py                       # نقطه ورود برنامه
└── requirements.txt              # وابستگی‌های پروژه

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation:**
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.

## Features

- User registration and login
- JWT token generation and validation
- User data retrieval

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.