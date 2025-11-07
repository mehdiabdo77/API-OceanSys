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


-- 🔹 SalesManager
INSERT INTO role_permission_tbl (role_id, permission_id) VALUES
(2, 2), (2, 3), (2, 4), (2, 5), (2, 7);

-- 🔹 FinanceManager
INSERT INTO role_permission_tbl (role_id, permission_id) VALUES
(3, 3), (3, 6), (3, 7);

-- 🔹 SalesAgent
INSERT INTO role_permission_tbl (role_id, permission_id) VALUES
(4, 2), (4, 3), (4, 4);


SELECT 1
    FROM permission_tbl p
    WHERE p.code = 1
      AND (
          p.id IN (
              SELECT permission_id
              FROM role_permission_tbl rp
              JOIN user_tbl u ON rp.role_id = u.role_id
              WHERE u.id = 1
          )
          OR p.id IN (
              SELECT permission_id
              FROM user_permission_tbl
              WHERE user_id = 1 AND grant_type = 'ALLOW'
          )
      )
      AND p.id NOT IN (
          SELECT permission_id
          FROM user_permission_tbl
          WHERE user_id = 1 AND grant_type = 'DENY'
      )
    LIMIT 1;


SELECT 
    p.code,
    CASE 
        WHEN up.grant_type = 'DENY' THEN  0
        WHEN up.grant_type = 'ALLOW' THEN  1
        WHEN rp.permission_id is not null THEN  1
        ELSE  0
    END as has_access
from permission_tbl as p
LEFT join user_permission_tbl as up 
    on up.permission_id = p.id and up.user_id=1
LEFT join user_tbl as u
    on u.id = 1
left join role_permission_tbl as rp 
    on rp.permission_id = p.id and rp.role_id = u.role_id



-- بررسی دسترسی های کاربر
SELECT 
    p.code,
    CASE
        WHEN rp.permission_id is not null THEN  1
        ELSE  0
    END as has_access
from permission_tbl as p
LEFT join user_tbl as u
    on u.id = 1
left join role_permission_tbl as rp 
    on rp.permission_id = p.id and rp.role_id = u.role_id


-- SELECT 
--     p.code,
--     CASE 
--         WHEN rp.permission_id is not null THEN  1
--         ELSE  0
--     END as has_access
-- from permission_tbl as p
-- LEFT join role_permission_tbl as rp on p.id = rp.permission_id
-- LEFT JOIN role_tbl AS r 
--     ON r.id = rp.role_id 
-- WHERE r.name = 'admin';

SELECT * from role_tbl

SELECT * from permission_tbl


SELECT
  p.code,
  CASE 
    WHEN EXISTS (
      SELECT 1
      FROM role_permission_tbl rp
      JOIN role_tbl r ON r.id = rp.role_id
      WHERE rp.permission_id = p.id
        AND r.name = 'SalesManager'
    ) THEN 1
    ELSE 0
  END AS has_access
FROM permission_tbl p
ORDER BY p.code;
