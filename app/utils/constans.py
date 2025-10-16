from enum import Enum

class Permissions(str, Enum):
    """
    فهرست کدهای دسترسی (Permissions) مورد استفاده در سیستم
    """

    USER_MANAGE = "USER_MANAGE"               # مدیریت کاربران
    CUSTOMER_SCAN = "CUSTOMER_SCAN"           # مشاهده/اسکن اطلاعات مشتری
    NEW_CUSTOMER = "NEW_CUSTOMER"             # ثبت مشتری جدید
    COMPETITOR_PRICES = "COMPETITOR_PRICES"   # مشاهده قیمت رقبا
