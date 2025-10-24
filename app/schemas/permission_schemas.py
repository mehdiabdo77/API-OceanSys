from pydantic import BaseModel
from typing import Optional

class PermissionEditSchemas(BaseModel):
     user_id: int
     permissions: list[dict] 
