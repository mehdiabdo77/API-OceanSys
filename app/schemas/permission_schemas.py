from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class PermissionItem(BaseModel):
    permission: str
    grant_type: str 


class PermissionEditSchemas(BaseModel):
    permissions: List[PermissionItem] = Field( 
        ..., 
        examples=[ 
            [ 
                {"permission": "CUSTOMER_SCAN", "grant_type": "ALLOW"}, 
                {"permission": "CUSTOMER_REGISTER", "grant_type": "DENY"} 
            ] 
        ] 
    ) 


class PermissionUserEditSchemas(PermissionEditSchemas):
    identifier: int = Field(..., examples=[1], description="شناسه کاربر")


class PermissionRoleEditSchemas(PermissionEditSchemas):
    identifier: str = Field(..., examples=["SalesManager"], description="نام نقش")


class PermissionSchema(BaseModel):
    id: int = Field(..., description="شناسه دسترسی")
    code: str = Field(..., description="کد دسترسی")
    name: str = Field(..., description="نام دسترسی")
    description: Optional[str] = Field(None, description="توضیحات دسترسی")


class RoleCreateSchema(BaseModel):
    name: str = Field(..., description="نام نقش (منحصر به فرد)", examples=["SalesManager"])
    description: Optional[str] = Field(None, description="توضیحات نقش")


class PermissionCreateSchema(BaseModel):
    code: str = Field(..., description="کد دسترسی (منحصر به فرد)", examples=["PRODUCT_MANAGE"])
    name: str = Field(..., description="نام دسترسی", examples=["مدیریت محصولات"])
    description: Optional[str] = Field(None, description="توضیحات دسترسی")


class RoleSchema(BaseModel):
    id: int = Field(..., description="شناسه نقش")
    name: str = Field(..., description="نام نقش")
    description: Optional[str] = Field(None, description="توضیحات نقش")

