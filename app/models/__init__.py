from app.models.user.user_model import UserModel
from app.models.user.role_model import RoleModel
from app.models.user.permission_model import PermissionModel
from app.models.user.role_permission_model import RolePermissionModel
from app.models.user.user_permission_model import UserPermissionModel
from app.models.customer_model import CustomerModel
from app.models.point_model import PointModel
from app.models.customer_analysis.disactive_description_model import DisActiveDescriptionModel
from app.models.customer_analysis.CRM_customer_description import CRMCustomerDescriptionModel
from app.models.customer_analysis.Customer_Idit import CustomerIditModel
from app.models.customer_analysis.product_category_customer import ProductCategoryCustomerModel
from app.models.customer_analysis.visit_report import VisitReportModel

__all__ = [
    "UserModel",
    "RoleModel",
    "PermissionModel",
    "RolePermissionModel",
    "UserPermissionModel",
    "CustomerModel",
    "PointModel",
    "DisActiveDescriptionModel",
    "CRMCustomerDescriptionModel",
    "CustomerIditModel",
    "ProductCategoryCustomerModel",
    "VisitReportModel"
]
