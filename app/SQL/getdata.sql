
CREATE TABLE visit_reports (
    id int AUTO_INCREMENT PRIMARY KEY,
    customer_id int not NULL,
    user_id int not NULL,
    edit_status TINYINT(1) NOT NULL DEFAULT 0,
    visit_status TINYINT(1) NOT NULL DEFAULT 0,
    visit_Date DATETIME DEFAULT NULL,
    user_idit_data DATETIME DEFAULT NULL,
    server_idit_data DATETIME DEFAULT null on UPDATE CURRENT_TIMESTAMP
)



CREATE TABLE visits (
    visit_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_code INT,
    visit_date VARCHAR(10),  -- فرمت: YYYY/MM/DD
    visited BOOLEAN DEFAULT 0,
    visitor_username VARCHAR(50),
    visit_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_code) REFERENCES customers(customer_code)
);




CREATE TABLE target_table AS
SELECT
    کد_مشتری AS customer_code,
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
FROM  dw_gazal.customer_tbl_main
WHERE واحد_سازمانی = 'مويرگي تهران'
LIMIT 10








CREATE TABLE DisActiveDescription (
    customer_code INT NOT NULL,
    Reason VARCHAR(255) NOT NULL,
    Description TEXT,
    PRIMARY KEY (customer_code),
    user_id INT,
    created_at DATETIME);



CREATE TABLE ProductCategoryCustomer(
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_code INT NOT NULL,
    sku VARCHAR(100) NOT NULL,
    user_id INT Not NULL,
    created_at DATETIME
);


CREATE TABLE CRMCustomerDescription (
    customer_code INT NOT NULL,
    description_crm TEXT NOT NULL,
    is_customer_visit TINYINT(1) DEFAULT 0,   -- آیا مشتری (فروشنده) خودش ویزیت/سرکشی می‌کند؟
    is_owner_in_shop TINYINT(1) DEFAULT 0,    -- آیا صاحب مغازه در مغازه هست؟
    is_cooperation TINYINT(1) DEFAULT 1,      -- آیا با ما همکاری می‌کند؟ (1 = بله, 0 = خیر)
    user_id INT Not NULL,
    created_at DATETIME
);



CREATE TABLE CustomerIditTBL (
    customer_code INT NOT NULL,
    national_code VARCHAR(12),
    role_code VARCHAR(20),
    postal_code VARCHAR(12),
    customer_board VARCHAR(255),
    customer_name VARCHAR(255),
    address TEXT,
    mobile_number VARCHAR(20),
    mobile_number2 VARCHAR(20),
    phone_number VARCHAR(20),
    store_area INT,
    user_id INT Not NULL,
    created_at DATETIME
)


CREATE TABLE  Point_tbl (
    customer_code INT,
    lat DECIMAL(9,6),
    lng DECIMAL(9,6),
    username VARCHAR(200),
    date_shamsi VARCHAR(20),
    date_miladi DATETIME
)


CREATE TABLE department_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE position_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL UNIQUE,
    level INT
);

CREATE TABLE user_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(200) UNIQUE NOT NULL,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    -- department_id INT NOT NULL, حذف میشود - از مدل حذف شود
    -- position_id INT NOT NULL, حذف میشود - از مدل حذف شود
    role_id INT NOT NULL,  -- هر کاربر دقیقا یک نقش دارد
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- ارتباط که باید بدم
    FOREIGN KEY (role_id) REFERENCES role_tbl(id) ON DELETE RESTRICT

);

CREATE TABLE role_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,    -- مثل "Admin", "ManagerFinance"
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permission_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(100) NOT NULL UNIQUE,    -- مثل: USER_MANAGE, UPLOAD_DATA
    name VARCHAR(100) NOT NULL,           -- عنوان فارسی مثل "مدیریت کاربران"
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_permission_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    permission_id INT NOT NULL,
    grant_type ENUM('ALLOW', 'DENY') DEFAULT 'ALLOW',  -- نوع مجوز: مجاز یا ممنوع
    FOREIGN KEY (user_id) REFERENCES user_tbl(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permission_tbl(id) ON DELETE CASCADE,
    UNIQUE (user_id, permission_id)
);

CREATE TABLE role_permission_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,

    FOREIGN KEY (role_id) REFERENCES role_tbl(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permission_tbl(id) ON DELETE CASCADE,

    UNIQUE (role_id, permission_id)  -- جلوگیری از تکرار
);



INSERT INTO role_tbl (id, name, description) VALUES
(1, 'Admin', 'دسترسی کامل به همه ماژول‌ها'),
(2, 'SalesManager', 'مدیر فروش - دسترسی فقط به ماژول‌های فروش'),
(3, 'FinanceManager', 'مدیر مالی - دسترسی به ماژول‌های مالی و گزارش‌ها'),
(4, 'SalesAgent', 'بازاریاب - دسترسی محدود برای ثبت مشتری و ارسال اطلاعات');

INSERT INTO permission_tbl (id, code, name, description) VALUES
(1, 'USER_MANAGE', 'مدیریت کاربران', 'ایجاد، حذف و ویرایش کاربران سیستم'),
(2, 'CUSTOMER_SCAN', 'اسکن مشتریان مسیر', 'دسترسی به ماژول بازرسی و اسکن مشتری'),
(3, 'UPLOAD_DATA', 'ارسال اطلاعات', 'امکان ارسال داده‌های ثبت نشده'),
(4, 'NEW_CUSTOMER', 'افزودن مشتری جدید', 'دسترسی به ثبت مشتری جدید'),
(5, 'COMPETITOR_PRICES', 'قیمت رقبا', 'مشاهده و ثبت قیمت رقبا'),
(6, 'FINANCE_REPORTS', 'گزارشات مالی', 'مشاهده گزارشات مالی'),
(7, 'VIEW_DASHBOARD', 'داشبورد مدیریتی', 'نمایش خلاصه وضعیت کل سیستم');

INSERT INTO role_permission_tbl (role_id, permission_id)
SELECT 1, id FROM permission_tbl;



ALTER TABLE customer
ADD COLUMN edit SMALLINT


UPDATE customer set datavisit = '1404/05/30'


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
    u.username AS username,
    v.`visit_Date`  as datavisit,
    v.user_idit_data as upload_date,
    v.visit_status as visited,
    v.edit_status as edit
FROM visit_reports as v 
join customer as c on v.customer_id = c.کد_مشتری
join user_tbl as u on u.id = v.user_id
WHERE v.`visit_Date` = (
    SELECT MAX(v.`visit_Date`) 
    FROM customer
);


INSERT INTO visit_reports(customer_id ,user_id , `visit_Date` )
SELECT کد_مشتری, u.user_id , '2025/9/11'
FROM customer c
CROSS JOIN user_tbl as u
WHERE مسیر = '11' AND u.username="m.abdollahi"

INSERT INTO visit_reports (customer_id, user_id, visit_Date)
SELECT c.کد_مشتری, u.id, '2025-09-11'
FROM customer c
CROSS JOIN user_tbl u
WHERE c.مسیر = '11'
AND u.username = "m.abdollahi";


SELECT DISTINCT مسیر as route_id, COUNT(کد_مشتری) as customer_count 
FROM customer
GROUP BY مسیر
ORDER BY مسیر

SELECT * FROM user_tbl WHERE user_tbl.username = 'm.abdollahi' LIMIT 1;
