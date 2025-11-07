from pydantic import BaseModel, Field
from typing import List, Dict

class PermissionItem(BaseModel):
    permission: str
    grant_type: str 


class PermissionUserEditSchemas(BaseModel):
    user_id: int = Field(..., examples=[1])
    permissions: List[PermissionItem] = Field(
        ...,
        examples=[
            [
               {"permission": "CUSTOMER_SCAN", "grant_type": "ALLOW"},
               {"permission": "CUSTOMER_REGISTER", "grant_type": "DENY"}
            ]
        ]
    )
