"""Usuario (User) models with security extensions."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Usuario(Base):
    """User model for authentication and authorization."""

    __tablename__ = "usuarios"
    # __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)  # company email
    email_personal: Mapped[str] = mapped_column(String(100), nullable=True)  # personal email
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)  # phone number
    dni: Mapped[str] = mapped_column(String(30), nullable=True, index=True)  # national ID
    iban: Mapped[str] = mapped_column(String(34), nullable=True)  # IBAN for payments
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=True)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=True)
    nombre_completo: Mapped[str] = mapped_column(String(100), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    es_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    anonimizado_en: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Role(Base):
    """Role model grouping permissions."""

    __tablename__ = "roles"
    __table_args__ = (UniqueConstraint("organization_id", "nombre", name="uix_role_org_nombre"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
    es_sistema: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Permission(Base):
    """Permission model with unique code."""

    __tablename__ = "permisos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
    # categoria: Mapped[str] = mapped_column(String(100), nullable=True, default="General")  # Discord-like grouping
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class RolePermission(Base):
    """Many-to-many between roles and permissions."""

    __tablename__ = "roles_permisos"
    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uix_role_permission"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("permisos.id"), nullable=False)


class UserRole(Base):
    """Many-to-many between users and roles."""

    __tablename__ = "usuarios_roles"
    __table_args__ = (UniqueConstraint("usuario_id", "role_id", name="uix_usuario_role"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)


class SoDRule(Base):
    """Segregation of Duties rule between two permission codes."""

    __tablename__ = "sod_rules"
    __table_args__ = (UniqueConstraint("organization_id", "perm_a", "perm_b", name="uix_sod_rule"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    perm_a: Mapped[str] = mapped_column(String(150), nullable=False)
    perm_b: Mapped[str] = mapped_column(String(150), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="high")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class SoDViolation(Base):
    """Segregation of Duties violation log."""

    __tablename__ = "sod_violations"
    __table_args__ = (Index("ix_sod_violation_org_user", "organization_id", "user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    attempted_permission: Mapped[str] = mapped_column(String(150), nullable=False)
    conflicting_permission: Mapped[str] = mapped_column(String(150), nullable=False)
    rule_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("sod_rules.id"), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
