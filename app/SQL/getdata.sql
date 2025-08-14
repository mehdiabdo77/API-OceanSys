-- Active: 1753974425566@@127.0.0.1@3306@ocean
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
LIMIT 10



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
    PRIMARY KEY (customer_code)
);


ALTER TABLE DisActiveDescription
ADD COLUMN username VARCHAR(255),
ADD COLUMN date_shamsi VARCHAR(20),
ADD COLUMN date_miladi DATETIME;



CREATE TABLE ProductCategoryCustomer(
    customer_code INT NOT NULL,
    sku VARCHAR(100) NOT NULL,
    username VARCHAR(255),
    date_shamsi VARCHAR(20),
    date_miladi DATETIME
);