from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base


class RolePermissionModel(Base):
   __tablename__ = "role_permission_tbl"

   id = Column(Integer, primary_key=True, autoincrement=True)
   role_id = Column(Integer, ForeignKey("role_tbl.id", ondelete="CASCADE"), nullable=False)
   permission_id = Column(Integer, ForeignKey("permission_tbl.id", ondelete="CASCADE"), nullable=False)

   role = relationship("RoleModel", back_populates="permissions")
   permission = relationship("PermissionModel", back_populates="roles")

   __table_args__ = (
        {'unique_constraint': ['role_id', 'permission_id']}
    )