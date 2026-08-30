# OceanSys API

سیستم مدیریت ارتباط با مشتری (CRM) و مدیریت بازدیدهای میدانی فروشندگان، که با فریم‌ورک **FastAPI** توسعه داده شده است. این API امکان مدیریت کاربران، مشتریان، نقش‌ها و دسترسی‌ها، ثبت بازدیدها و مدیریت مسیرهای بازدید را فراهم می‌کند.

---

## فهرست مطالب

- [ویژگی‌ها](#ویژگی‌ها)
- [معماری پروژه](#معماری-پروژه)
- [ساختار کامل پروژه](#ساختار-کامل-پروژه)
- [پیش‌نیازها](#پیش‌نیازها)
- [راه‌اندازی پروژه](#راه‌اندازی-پروژه)
- [تنظیمات محیطی](#تنظیمات-محیطی)
- [دیتابیس](#دیتابیس)
- [احراز هویت و سیستم دسترسی‌ها](#احراز-هویت-و-سیستم-دسترسی‌ها)
- [مستندات API](#مستندات-api)
- [Endpoint ها به تفکیک ماژول](#endpoint-ها-به-تفکیک-ماژول)
  - [Auth (احراز هویت)](#auth-احراز-هویت)
  - [User (مدیریت کاربران)](#user-مدیریت-کاربران)
  - [Permission (نقش و دسترسی)](#permission-نقش-و-دسترسی)
  - [Customer (مدیریت مشتریان)](#customer-مدیریت-مشتریان)
  - [Point (ثبت موقعیت جغرافیایی)](#point-ثبت-موقعیت-جغرافیایی)
  - [Visit (مسیرها و بازدیدها)](#visit-مسیرها-و-بازدیدها)
  - [Job User (برنامه‌ریزی مسیر بازدید)](#job-user-برنامهریزی-مسیر-بازدید)
- [مدل‌های دیتابیس](#مدل‌های-دیتابیس)
- [اجرای پروژه](#اجرای-پروژه)
- [تست API با Swagger](#تست-api-با-swagger)
- [وابستگی‌ها](#وابستگی‌ها)
- [رفع مشکلات رایج](#رفع-مشکلات-رایج)

---

## ویژگی‌ها

- ✅ **احراز هویت JWT** با توکن Bearer و زمان انقضا قابل تنظیم
- ✅ **مدیریت کاربران** با امکان فعال/غیرفعال کردن، تغییر نقش و ثبت کاربر جدید
- ✅ **سیستم نقش و دسترسی RBAC** (Role-Based Access Control) با امکان تعریف نقش‌های دلخواه و اختصاص دسترسی‌های سطحی به کاربران و نقش‌ها
- ✅ **مدیریت مشتریان** شامل مشاهده اطلاعات کامل، ویرایش اطلاعات، ثبت توضیحات CRM، دسته‌بندی محصولات و غیرفعال‌سازی
- ✅ **ثبت گزارش بازدید** از مشتریان توسط فروشندگان
- ✅ **ثبت موقعیت جغرافیایی** (GPS) فروشندگان هنگام بازدید
- ✅ **مدیریت مسیرهای بازدید** و برنامه‌ریزی روزانه فروشندگان
- ✅ **ایجاد خودکار دیتابیس** در صورت عدم وجود (با Persian Collation)
- ✅ **ایجاد خودکار جداول** از روی مدل‌های SQLAlchemy
- ✅ **پشتیبانی از تاریخ شمسی** با استفاده از کتابخانه jdatetime
- ✅ **مستندات خودکار API** با Swagger UI و ReDoc

---

## معماری پروژه

پروژه بر اساس معماری **Layered Architecture** یا **سه‌لایه‌ای** سازماندهی شده است:

```
┌──────────────────────────────────────────────────┐
│                  Routes (Presentation)           │
│  تعریف endpoint ها، دریافت و پاسخ به درخواست‌ها  │
├──────────────────────────────────────────────────┤
│                  Services (Business Logic)       │
│  منطق تجاری، عملیات روی داده‌ها، قوانین کسب      │
├──────────────────────────────────────────────────┤
│             Models / DB (Data Access)            │
│  مدل‌های SQLAlchemy، اتصال و کوئری به دیتابیس    │
└──────────────────────────────────────────────────┘
```

### جریان یک درخواست:

1. درخواست HTTP به **Route** مربوطه می‌رسد
2. در صورت نیاز، **Authentication** و **Authorization** بررسی می‌شود
3. داده‌های ورودی با **Schemas (Pydantic)** اعتبارسنجی می‌شوند
4. Route درخواست را به **Service** مربوطه می‌سپارد
5. Service منطق تجاری را اجرا کرده و از **Models** برای دسترسی به دیتابیس استفاده می‌کند
6. پاسخ به صورت JSON به کاربر بازگردانده می‌شود

---

## ساختار کامل پروژه

```
API - OceanSys/
├── app/
│   ├── auth/
│   │   ├── auth_handler.py       # مدیریت توکن JWT، احراز هویت، get_current_user
│   │   └── permissions.py        # Decorator بررسی دسترسی (permission_required)
│   ├── core/
│   │   ├── base.py               # کانکشن دیتابیس، engine، Base، SessionLocal
│   │   ├── config.py             # بارگذاری تنظیمات از فایل .env
│   │   └── db_setup.py           # ایجاد خودکار دیتابیس و جداول
│   ├── models/                   # مدل‌های SQLAlchemy (ORM)
│   │   ├── customer_analysis/
│   │   │   ├── CRM_customer_description.py   # توضیحات CRM مشتری
│   │   │   ├── Customer_Idit.py              # تاریخچه ویرایش اطلاعات مشتری
│   │   │   ├── disactive_description_model.py # توضیحات غیرفعال‌سازی
│   │   │   ├── product_category_customer.py  # دسته‌بندی محصولات مشتری
│   │   │   └── visit_report.py               # گزارش بازدید از مشتری
│   │   ├── user/
│   │   │   ├── permission_model.py           # مدل دسترسی (Permission)
│   │   │   ├── role_model.py                 # مدل نقش (Role)
│   │   │   ├── role_permission_model.py      # ارتباط نقش و دسترسی (M:N)
│   │   │   ├── user_model.py                 # مدل کاربر
│   │   │   └── user_permission_model.py      # ارتباط کاربر و دسترسی (M:N)
│   │   ├── __init__.py
│   │   ├── customer_model.py     # مدل مشتری اصلی
│   │   └── point_model.py        # مدل ثبت موقعیت جغرافیایی
│   ├── routes/                   # تعریف endpoint ها
│   │   ├── auth_router.py        # روت‌های احراز هویت (login / token)
│   │   ├── user_route.py         # روت‌های مدیریت کاربران
│   │   ├── permission_route.py   # روت‌های نقش و دسترسی
│   │   ├── Customer.py           # روت‌های مدیریت مشتریان
│   │   ├── New_Customer.py       # روت‌های مشتری جدید
│   │   ├── point.py              # روت ثبت موقعیت GPS
│   │   ├── visit.py              # روت‌های مسیرها و بازدیدها
│   │   └── user_job.py           # روت‌های برنامه‌ریزی مسیر بازدید
│   ├── schemas/                  # مدل‌های Pydantic برای اعتبارسنجی ورودی/خروجی
│   │   ├── customer_schemas.py   # Schema های مربوط به مشتری
│   │   ├── permission_schemas.py # Schema های نقش و دسترسی
│   │   ├── post_schemas.py       # Schema های ثبت موقعیت و مسیر
│   │   ├── response_schemas.py   # Schema های پاسخ سرور
│   │   └── user_schemas.py       # Schema های کاربر
│   ├── services/                 # منطق تجاری (Business Logic)
│   │   ├── customer_service.py   # عملیات مربوط به مشتری
│   │   ├── job_user_service.py   # عملیات برنامه‌ریزی مسیر
│   │   ├── permission_service.py # عملیات نقش و دسترسی
│   │   ├── point_service.py      # عملیات ثبت موقعیت
│   │   ├── route_service.py      # عملیات مسیر بازدید
│   │   └── user_service.py       # عملیات کاربران
│   └── utils/                    # ابزارهای کمکی
│       ├── constans.py           # مقادیر ثابت (Permissions Enum, RoleName Enum)
│       └── security.py           # توابع هش رمز عبور و تایید آن
├── main.py                       # نقطه ورود FastAPI (ایجاد app و include routerها)
├── requirements.txt              # لیست وابستگی‌ها
├── .env.example                  # نمونه فایل تنظیمات محیطی
├── .gitignore
└── README.md
```

---

## پیش‌نیازها

برای اجرای این پروژه به نرم‌افزارهای زیر نیاز دارید:

| نرم‌افزار | نسخه پیشنهادی | توضیحات |
|----------|--------------|---------|
| Python | 3.10+ | زبان برنامه‌نویسی اصلی پروژه |
| SQL Server | 2019+ | دیتابیس رابطه‌ای پروژه |
| ODBC Driver 17 for SQL Server | 17.x | درایور اتصال به SQL Server |
| pip | آخرین نسخه | مدیریت پکیج‌های Python |

### نصب ODBC Driver 17 (ویندوز):

1. به آدرس زیر بروید:
   [Microsoft ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
2. نسخه ویندوز را دانلود و نصب کنید.

---

## راه‌اندازی پروژه

### قدم ۱: کلون کردن مخزن

```bash
git clone <repository-url>
cd "API - OceanSys"
```

### قدم ۲: ساخت محیط مجازی (Virtual Environment)

**ویندوز (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

پس از فعال شدن محیط مجازی، ابتدای خط فرمان شما `(venv)` نمایش داده می‌شود.

### قدم ۳: نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### قدم ۴: تنظیم فایل محیطی (.env)

فایل `.env.example` را کپی کرده و نام آن را به `.env` تغییر دهید:

**ویندوز (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

سپس مقادیر داخل فایل `.env` را با مقادیر واقعی خود جایگزین کنید (جزئیات در بخش بعد).

### قدم ۵: اطمینان از اجرای SQL Server

اطمینان حاصل کنید که سرویس SQL Server در حال اجرا است و اطلاعات لاگین (User/Password) در فایل `.env` به درستی تنظیم شده است.

### قدم ۶: اجرای پروژه

```bash
uvicorn main:app --reload
```

پروژه به صورت پیش‌فرض روی آدرس زیر اجرا می‌شود:
```
http://127.0.0.1:8000
```

> 💡 هنگام اولین اجرا، دیتابیس و تمام جداول به صورت خودکار ایجاد می‌شوند.

---

## تنظیمات محیطی

تمام تنظیمات پروژه از طریق متغیرهای محیطی (Environment Variables) و فایل `.env` مدیریت می‌شوند. فایل `.env.example` شامل تمام متغیرهای مورد نیاز است:

| متغیر | مقدار پیش‌فرض | توضیحات |
|-------|--------------|---------|
| `SECRET_KEY` | `your-secret-key-here` | کلید مخفی برای امضای توکن‌های JWT. **حتماً در محیط تولید به یک رشته قوی و تصادفی تغییر دهید.** |
| `ALGORITHM` | `HS256` | الگوریتم رمزنگاری توکن JWT. پیشنهاد: تغییر ندهید. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `9000` | زمان انقضا توکن دسترسی به دقیقه. پیش‌فرض ≈ 6 روز. |
| `DB_DRIVER` | `ODBC Driver 17 for SQL Server` | نام درایور ODBC نصب شده. |
| `DB_SERVER` | `127.0.0.1` | آدرس سرور SQL Server (می‌تواند `localhost` یا IP سرور باشد). |
| `DB_PORT` | `1433` | پورت اتصال به SQL Server (پورت پیش‌فرض). |
| `DB_DATABASE` | `ocean` | نام دیتابیس پروژه (در صورت عدم وجود، به صورت خودکار ساخته می‌شود). |
| `DB_USER` | `sa` | نام کاربری اتصال به SQL Server. |
| `DB_PASSWORD` | `your-db-password-here` | رمز عبور کاربر SQL Server. |

> ⚠️ **هشدار امنیتی:** هرگز فایل `.env` حاوی مقادیر واقعی را به مخزن Git کامیت نکنید. این فایل در `.gitignore` قرار گرفته است.

---

## دیتابیس

### نوع دیتابیس
پروژه از **Microsoft SQL Server** به عنوان دیتابیس اصلی استفاده می‌کند و ارتباط از طریق **pyodbc + SQLAlchemy** برقرار می‌شود.

### ایجاد خودکار دیتابیس
هنگام راه‌اندازی پروژه، تابع `initialize_database()` در [db_setup.py](file:///e:/projects/api/API%20-%20OceanSys/app/core/db_setup.py) اجرا می‌شود:

1. ابتدا به دیتابیس `master` متصل می‌شود
2. بررسی می‌کند که آیا دیتابیس با نام مشخص شده در `DB_DATABASE` وجود دارد یا خیر
3. در صورت عدم وجود، دیتابیس را با **Collation** زیر ایجاد می‌کند:
   ```
   Persian_100_CI_AI
   ```
   این collation از حروف فارسی به درستی پشتیبانی می‌کند و مشکل ذخیره کاراکترهای فارسی را حل می‌کند.
4. پس از اطمینان از وجود دیتابیس، با استفاده از `Base.metadata.create_all()` تمام جداول از روی مدل‌ها ساخته می‌شوند.

### Schema های دیتابیس

| Schema | جدول‌ها | توضیحات |
|--------|---------|---------|
| `Security` | `UserAccount`, `Role`, `Permission`, `RolePermission`, `UserPermission` | جداول مربوط به کاربران و امنیت |
| (Default) | `customer`, `Point_tbl`, و جداول `customer_analysis` | جداول مربوط به مشتریان و عملیات تجاری |

---

## احراز هویت و سیستم دسترسی‌ها

### احراز هویت (Authentication)
پروژه از **JWT (JSON Web Token)** با الگوی **Bearer Token** استفاده می‌کند.

#### نحوه دریافت توکن:
درخواست POST به endpoint `/token` ارسال کنید (جزئیات در بخش API).

#### نحوه استفاده از توکن:
در تمام درخواست‌هایی که نیاز به احراز هویت دارند، توکن را در هدر درخواست قرار دهید:
```http
Authorization: Bearer <your-access-token>
```

### سیستم دسترسی‌ها (Authorization)
سیستم دسترسی‌ها بر اساس **RBAC (Role-Based Access Control)** پیاده‌سازی شده است:

- هر **کاربر** می‌تواند **یک نقش** داشته باشد (Role)
- هر **نقش** می‌تواند **چند دسترسی** داشته باشد
- علاوه بر آن، می‌توان دسترسی مستقیم به **کاربر** نیز اختصاص داد (override نقش)
- نوع هر دسترسی می‌تواند `GRANT` (اجازه) یا `DENY` (ممانعت) باشد

### لیست دسترسی‌های سیستم (Permissions Enum)
در فایل [constans.py](file:///e:/projects/api/API%20-%20OceanSys/app/utils/constans.py) تعریف شده‌اند:

| کد دسترسی | توضیحات |
|-----------|---------|
| `USER_MANAGE` | مدیریت کاربران (ثبت، ویرایش، تغییر نقش، فعال/غیرفعال) |
| `CUSTOMER_SCAN` | مشاهده و اسکن اطلاعات مشتری، ویرایش، ثبت توضیحات |
| `NEW_CUSTOMER` | ثبت مشتری جدید |
| `COMPETITOR_PRICES` | مشاهده قیمت رقبا |
| `ROLE_MANAGE` | مدیریت نقش‌ها |
| `PERMISSION_MANAGE` | مدیریت دسترسی‌ها |
| `JOB_ROUTE` | برنامه‌ریزی و تخصیص مسیر بازدید به فروشندگان |

### نقش‌های پیش‌فرض:
| نام نقش | توضیحات |
|---------|---------|
| `admin` | مدیر سیستم - تمامی دسترسی‌ها را دارد |
| `user` | کاربر عادی - معمولاً فروشنده |

---

## مستندات API

پروژه به صورت خودکار مستندات تعاملی API را تولید می‌کند:

| ابزار | آدرس | توضیحات |
|------|------|---------|
| **Swagger UI** | `http://127.0.0.1:8000/docs` | رابط کاربری زیبا برای تست و مشاهده endpoint ها |
| **ReDoc** | `http://127.0.0.1:8000/redoc` | مستندات با ظاهر مدرن و مناسب اشتراک‌گذاری |
| **OpenAPI Schema** | `http://127.0.0.1:8000/openapi.json` | خروجی JSON استاندارد OpenAPI |

> 💡 توصیه می‌شود برای آشنایی با endpoint ها، ابتدا به آدرس Swagger UI مراجعه کنید و مستقیماً API ها را تست کنید.

---

## Endpoint ها به تفکیک ماژول

### Auth (احراز هویت)

**Tag:** `auth`

| متد HTTP | Endpoint | توضیحات | دسترسی لازم |
|---------|----------|---------|------------|
| `POST` | `/token` | دریافت توکن دسترسی (لاگین) | ندارد (عمومی) |

#### نمونه درخواست `/token`:
- **نوع درخواست:** `application/x-www-form-urlencoded`
- **پارامترها:**
  - `username`: نام کاربری
  - `password`: رمز عبور
- **پاسخ موفق (200):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **خطا (401):** اطلاعات کاربری نامعتبر

---

### User (مدیریت کاربران)

**Tag:** `user`

| متد HTTP | Endpoint | توضیحات | دسترسی لازم |
|---------|----------|---------|------------|
| `POST` | `/setup-first-user` | ثبت کاربر اول سیستم (ادمین) | ندارد (فقط وقتی سیستم کاربری ندارد) |
| `POST` | `/register` | ثبت کاربر جدید | `USER_MANAGE` |
| `GET` | `/getUserdata` | دریافت اطلاعات کاربر فعلی | فقط احراز هویت |
| `GET` | `/getAllUserdata` | دریافت لیست تمام کاربران | `USER_MANAGE` |
| `PATCH` | `/{username}/status` | فعال یا غیرفعال کردن کاربر | `USER_MANAGE` |

#### `/setup-first-user` - ثبت کاربر اول:
این endpoint فقط **یک بار** و هنگامی که سیستم هیچ کاربری ندارد کار می‌کند. کاربر اول به طور خودکار نقش `ADMIN` می‌گیرد.

**بدنه درخواست:**
```json
{
  "username": "admin",
  "first_name": "مدیر",
  "last_name": "سیستم",
  "password": "Admin@123",
  "isactive": true
}
```

---

### Permission (نقش و دسترسی)

**Tag:** `permission`

| متد HTTP | Endpoint | توضیحات | دسترسی لازم |
|---------|----------|---------|------------|
| `POST` | `/get_permission` | دریافت دسترسی‌های کاربر فعلی | فقط احراز هویت |
| `GET` | `/get_role_list` | دریافت لیست نقش‌های سیستم | `USER_MANAGE` |
| `GET` | `/get_permission_list` | دریافت لیست تمام دسترسی‌ها | `USER_MANAGE` |
| `GET` | `/get_all_roles_permissions` | دریافت دسترسی‌های تمام نقش‌ها | `USER_MANAGE` |
| `POST` | `/create_role` | ایجاد نقش جدید | `USER_MANAGE` |
| `POST` | `/create_permission` | ایجاد دسترسی جدید | `USER_MANAGE` |
| `PUT` | `/edit_permission_user` | ویرایش دسترسی‌های کاربران | `USER_MANAGE` |
| `PUT` | `/edit_permission_role` | ویرایش دسترسی‌های نقش‌ها | `USER_MANAGE` |
| `PATCH` | `/change_user_role` | تغییر نقش یک کاربر | `USER_MANAGE` |

---

### Customer (مدیریت مشتریان)

**Tag:** `customer`

| متد HTTP | Endpoint | توضیحات | دسترسی لازم |
|---------|----------|---------|------------|
| `GET` | `/getCustomerData` | دریافت اطلاعات کامل مشتریان | `CUSTOMER_SCAN` |
| `POST` | `/editcoustomerinfo` | ویرایش اطلاعات مشتری | `CUSTOMER_SCAN` |
| `POST` | `/disActiveCustomer` | غیرفعال کردن مشتری با ثبت توضیحات | `CUSTOMER_SCAN` |
| `POST` | `/ProductCategory` | ثبت دسته‌بندی محصولات برای مشتری | `CUSTOMER_SCAN` |
| `POST` | `/CRMCustomerDescription` | ثبت توضیحات/یادداشت CRM مشتری | `CUSTOMER_SCAN` |
| `POST` | `/task_complete` | علامت‌گذاری بازدید به عنوان تکمیل شده | فقط احراز هویت |

> 💡 نکته: هنگام ویرایش اطلاعات، غیرفعال کردن، ثبت دسته‌بندی و یا ثبت توضیحات CRM، وضعیت `isvisit` (وضعیت بازدید) مشتری به طور خودکار به‌روزرسانی می‌شود.

---

### Point (ثبت موقعیت جغرافیایی)

**Tag:** `point`

| متد HTTP | Endpoint | توضیحات | دسترسی لازم |
|---------|----------|---------|------------|
| `POST` | `/point` | ثبت موقعیت جغرافیایی فروشنده هنگام بازدید | فقط احراز هویت |

**بدنه درخواست نمونه:**
```json
{
  "customer_code": 1001,
  "lat": 35.6892,
  "lng": 51.3890,
  "date_shamsi": "1403/06/08",
  "date_miladi": "2024-08-30T10:30:00"
}
```

---

### Visit (مسیرها و بازدیدها)

**Tag:** `visit`

| متد HTTP | Endpoint | توضیحات | دسترسی لازم |
|---------|----------|---------|------------|
| `GET` | `/routes` | دریافت لیست تمام مسیرهای موجود | فقط احراز هویت |
| `POST` | `/update-route` | تخصیص مسیر به فروشنده (اپدیت مسیر) | فقط احراز هویت |

---

### Job User (برنامه‌ریزی مسیر بازدید)

**Tag:** `job_user`

| متد HTTP | Endpoint | توضیحات | دسترسی لازم |
|---------|----------|---------|------------|
| `POST` | `/set_rout` | تخصیص مشتری/مسیر به فروشنده در تاریخ مشخص | `JOB_ROUTE` |
| `DELETE` | `/del_rout` | حذف تخصیص مسیر از فروشنده | `JOB_ROUTE` |

---

## مدل‌های دیتابیس

در زیر معرفی کوتاه مدل‌های اصلی دیتابیس آمده است:

### کاربران و امنیت (Schema: Security)

| جدول | فیلدهای اصلی | توضیحات |
|------|-------------|---------|
| `UserAccount` | `id`, `username`, `first_name`, `last_name`, `password_hash`, `is_active`, `role_id`, `created_at` | اطلاعات کاربران سیستم |
| `Role` | `id`, `name`, `description` | نقش‌های سیستم (admin, user و ...) |
| `Permission` | `id`, `code`, `name`, `description` | لیست دسترسی‌ها (USER_MANAGE و ...) |
| `RolePermission` | `role_id`, `permission_id`, `grant_type` | ارتباط بین نقش و دسترسی (M:N) |
| `UserPermission` | `user_id`, `permission_id`, `grant_type` | دسترسی مستقیم به کاربر (جایگزین نقش) |

### مشتریان و عملیات تجاری

| جدول | فیلدهای اصلی | توضیحات |
|------|-------------|---------|
| `customer` | `customer_code` (PK), `customer_name`, `customer_board`, `national_code`, `area`, `zone`, `route`, `latitude`, `longitude`, `status`, `address`, `phone`, `mobile`, `postal_code`, `region` | اطلاعات اصلی مشتری |
| `Point_tbl` | `customer_code` (PK), `lat`, `lng`, `username`, `date_shamsi`, `date_miladi` | موقعیت جغرافیایی ثبت شده هنگام بازدید |
| `CustomerIditTable` (Customer_Idit) | تاریخچه ویرایش اطلاعات مشتری | هر بار که اطلاعات مشتری ویرایش می‌شود، یک رکورد در این جدول ذخیره می‌گردد |
| `DisActiveDescriptionTable` | توضیحات غیرفعال‌سازی مشتری | هنگام غیرفعال کردن مشتری، دلیل آن ذخیره می‌شود |
| `CRM_Customer_Description` | توضیحات و یادداشت‌های CRM | یادداشت‌های فروشنده در مورد مشتری در هر بازدید |
| `ProductCategoryCustomer` | دسته‌بندی محصولات مشتری | ثبت محصولات و دسته‌بندی‌های خریداری شده توسط مشتری |
| `VisitReportTable` | گزارش بازدید | گزارش کامل بازدید فروشنده از مشتری |

---

## اجرای پروژه

### حالت توسعه (Development):
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- پارامتر `--reload`: هنگام تغییر کد، سرور به صورت خودکار ری‌استارت می‌شود (فقط برای توسعه).
- پارامتر `--host 0.0.0.0`: دسترسی از طریق شبکه LAN را ممکن می‌سازد.
- پارامتر `--port`: تغییر پورت پیش‌فرض.

### حالت تولید (Production):
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

یا استفاده از Gunicorn (در لینوکس):
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## تست API با Swagger

1. پروژه را اجرا کنید:
   ```bash
   uvicorn main:app --reload
   ```

2. مرورگر خود را باز کرده و به آدرس زیر بروید:
   ```
   http://127.0.0.1:8000/docs
   ```

3. اگر اولین بار است که پروژه را اجرا می‌کنید، ابتدا کاربر اول را ثبت کنید:
   - endpoint `POST /setup-first-user` را باز کنید
   - روی **Try it out** کلیک کنید
   - اطلاعات کاربر ادمین را وارد کرده و **Execute** را بزنید

4. حالا لاگین کنید و توکن دریافت کنید:
   - endpoint `POST /token` را باز کنید
   - **Try it out** → نام کاربری و رمز عبور را وارد کنید → **Execute**
   - از بخش پاسخ، مقدار `access_token` را کپی کنید

5. در بالای صفحه Swagger، روی دکمه **Authorize** 🔒 کلیک کنید:
   - مقدار را به صورت زیر وارد کنید:
     ```
     Bearer <توکن-کپی-شده>
     ```
   - روی **Authorize** و سپس **Close** کلیک کنید.

6. تمام! حالا می‌توانید تمام endpoint ها را مستقیماً از داخل Swagger تست کنید.

---

## وابستگی‌ها

تمام پکیج‌های مورد نیاز در فایل [requirements.txt](file:///e:/projects/api/API%20-%20OceanSys/requirements.txt) لیست شده‌اند:

| پکیج | نسخه | کاربرد |
|------|------|--------|
| `fastapi` | 0.117.1 | فریم‌ورک اصلی ساخت API |
| `uvicorn` | 0.23.2 | سرور ASGI برای اجرای FastAPI |
| `sqlalchemy` | 2.0.20 | ORM برای ارتباط با دیتابیس |
| `pyodbc` | 5.0.1 | درایور اتصال به SQL Server |
| `pydantic` | 2.3.0 | اعتبارسنجی داده‌ها (Schemas) |
| `python-jose` | 3.3.0 | ساخت و تایید توکن‌های JWT |
| `passlib` | 1.7.4 | هش کردن امن رمز عبور (BCrypt) |
| `python-multipart` | 0.0.6 | پشتیبانی از فرم داده‌ها (برای endpoint /token) |
| `python-dotenv` | 1.0.0 | بارگذاری متغیرهای محیطی از فایل .env |
| `jdatetime` | 4.1.1 | تبدیل و کار با تاریخ شمسی |
| `pandas` | 2.1.0 | پردازش داده‌ها و کار با فایل‌های اکسل |
| `openpyxl` | 3.1.2 | خواندن و نوشتن فایل‌های Excel |

برای نصب مجدد:
```bash
pip install -r requirements.txt
```

برای آپدیت لیست وابستگی‌ها:
```bash
pip freeze > requirements.txt
```

---

## رفع مشکلات رایج

### ❌ خطا در اتصال به SQL Server

**علائم:**
```
pyodbc.InterfaceError: ('IM002', '[IM002] [Microsoft][ODBC Driver Manager] Data source name not found...')
```

**راه حل:**
1. اطمینان حاصل کنید **ODBC Driver 17 for SQL Server** نصب شده است.
2. بررسی کنید نام درایور در `.env` درست است (برای نسخه 17: `ODBC Driver 17 for SQL Server`).
3. اطمینان حاصل کنید سرویس SQL Server در حال اجرا است:
   - در ویندوز: `services.msc` → SQL Server → Start

---

### ❌ خطای رمز عبور یا لاگین SQL

**علائم:**
```
Login failed for user 'sa'
```

**راه حل:**
1. بررسی کنید `DB_USER` و `DB_PASSWORD` در فایل `.env` درست است.
2. اطمینان حاصل کنید که حالت احراز هویت SQL Server روی **SQL Server and Windows Authentication mode** تنظیم شده است.
3. در صورت استفاده از اکانت `sa`، از فعال بودن آن اطمینان حاصل کنید.

---

### ❌ خطای SECRET_KEY خالی

**علائم:**
```
TypeError: secret must be str or dict, not NoneType
```

**راه حل:**
فایل `.env` را ساخته و مقدار `SECRET_KEY` را در آن تنظیم کنید. برای تولید کلید امن می‌توانید از این دستور استفاده کنید:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

### ❌ خطای مشکل در نمایش حروف فارسی (?????)

**راه حل:**
1. دیتابیس را حذف کنید تا دوباره به صورت خودکار با `Persian_100_CI_AI` ساخته شود.
2. یا دستی collation دیتابیس و جداول را به `Persian_100_CI_AI` تغییر دهید.

---

### ❌ پورت 8000 اشغال است

**علائم:**
```
OSError: [WinError 10048] Only one usage of each socket address...
```

**راه حل:**
- پورت دیگری استفاده کنید:
  ```bash
  uvicorn main:app --reload --port 8080
  ```
- یا فرآیندی که روی 8000 اجرا شده را ببندید.

---

## نحوه شروع سریع (Quick Start Checklist)

- [ ] Python 3.10+ نصب شده است
- [ ] SQL Server و ODBC Driver 17 نصب شده‌اند
- [ ] مخزن کلون شده
- [ ] Virtual Environment ساخته و فعال شده
- [ ] وابستگی‌ها با `pip install -r requirements.txt` نصب شده‌اند
- [ ] فایل `.env` ساخته و مقادیر آن تنظیم شده است
- [ ] پروژه با `uvicorn main:app --reload` اجرا شده
- [ ] کاربر اول از طریق `/setup-first-user` ثبت شده
- [ ] به `http://127.0.0.1:8000/docs` رفته و لاگین کرده‌اید

---

## مشارکت در توسعه

برای مشارکت:
1. یک Fork از مخزن بسازید
2. یک Branch برای ویژگی جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات خود را کامیت کنید (`git commit -m 'Add some amazing feature'`)
4. به Branch اصلی Push کنید (`git push origin feature/amazing-feature`)
5. یک Pull Request باز کنید

---

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای جزئیات فایل LICENSE را مشاهده کنید.
