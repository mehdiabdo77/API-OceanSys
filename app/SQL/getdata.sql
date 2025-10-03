
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



CREATE TABLE CustomerIditTabel (
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
    username VARCHAR(200),
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
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at_jalali VARCHAR(10) NOT NULL,
    updated_at_jalali VARCHAR(10) NOT NULL,
    
    CONSTRAINT fk_department
        FOREIGN KEY (department_id) 
        REFERENCES department_tbl(id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_position
        FOREIGN KEY (position_id) 
        REFERENCES position_tbl(id)
        ON DELETE RESTRICT
);



-- درج داده به جداول parent اول
INSERT INTO department_tbl (name, description) VALUES 
('برنامه ریزی', 'واحد برنامه ریزی ستاد ');


INSERT INTO position_tbl (title, level) VALUES 
('مدیر', 1),
('کارشناس', 3),
('سرپرست', 2);



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
