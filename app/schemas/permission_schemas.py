from pydantic import BaseModel, Field
from typing import List, Dict

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

