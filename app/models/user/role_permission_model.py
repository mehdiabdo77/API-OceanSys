from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.base import Base


class RolePermissionModel(Base):
    __tablename__ = "RolePermission"
    __table_args__ = (
        UniqueConstraint('role_id', 'permission_id', name='uq_role_permission'),
        {"schema": "Security"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("security.Role.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("security.Permission.id", ondelete="CASCADE"), nullable=False)

    role = relationship("RoleModel", back_populates="permissions")
    permission = relationship("PermissionModel", back_populates="roles")
