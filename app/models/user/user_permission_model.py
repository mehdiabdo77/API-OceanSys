from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.models.user.permission_model import PermissionModel  # اضافه کردن این import
import enum

class GrantType(enum.Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"

class UserPermissionModel(Base):
    __tablename__ = "user_permission_tbl"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_tbl.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permission_tbl.id", ondelete="CASCADE"), nullable=False)
    grant_type = Column(Enum(GrantType), default=GrantType.ALLOW)

    user = relationship("UserModel", back_populates="permissions")
    permission = relationship(PermissionModel, back_populates="users")  # تغییر به استفاده مستقیم از کلاس

    __table_args__ = (
        {'unique_constraint': ['user_id', 'permission_id']}
    )