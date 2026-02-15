"""Tenant/Organization models for multi-tenancy."""

from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dario_app.database import Base


class Organization(Base):
    """Organization/Tenant model for multi-tenancy."""

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Business info
    tipo_negocio: Mapped[str] = mapped_column(
        String(100), nullable=True
    )  # retail, restaurante, etc
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)

    # Fiscal/Legal data (required for paid plans) - SPAIN COMPLIANCE
    razon_social: Mapped[str] = mapped_column(String(255), nullable=True)  # Razón social
    nif_cif: Mapped[str] = mapped_column(String(20), nullable=True, index=True)  # NIF/CIF/NIE
    nif_valido: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )  # Validated NIF

    # Fiscal address (required)
    domicilio_fiscal: Mapped[str] = mapped_column(Text, nullable=True)  # Calle, número
    municipio: Mapped[str] = mapped_column(String(100), nullable=True)  # Municipio
    provincia: Mapped[str] = mapped_column(String(100), nullable=True)  # Provincia/CCAA
    codigo_postal: Mapped[str] = mapped_column(String(20), nullable=True)  # CP (5 dígitos)
    pais: Mapped[str] = mapped_column(String(100), default="España", nullable=True)

    # Tax settings (required)
    regimen_iva: Mapped[str] = mapped_column(
        String(50), default="normal", nullable=True
    )  # normal, intracomunitario, exportación
    porcentaje_iva: Mapped[int] = mapped_column(
        Integer, default=21, nullable=False
    )  # 21%, 10%, 4%, etc
    aplica_irpf: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )  # Retención IRPF
    porcentaje_irpf: Mapped[int] = mapped_column(Integer, default=15, nullable=True)  # 15% default

    website: Mapped[str] = mapped_column(String(255), nullable=True)
    datos_fiscales_completos: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Contact
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    telefono: Mapped[str] = mapped_column(String(50), nullable=True)
    direccion: Mapped[str] = mapped_column(Text, nullable=True)

    # Subscription
    plan: Mapped[str] = mapped_column(
        String(50), nullable=False, default="trial"
    )  # trial, basic, pro, enterprise
    estado: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active"
    )  # active, suspended, cancelled
    trial_hasta: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Limits
    max_usuarios: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    max_productos: Mapped[int] = mapped_column(Integer, nullable=False, default=500)
    max_sucursales: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Settings
    configuracion: Mapped[str] = mapped_column(Text, nullable=True)  # JSON settings
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relaciones
    eventos: Mapped[List["Evento"]] = relationship(
        "Evento", back_populates="organization", cascade="all, delete-orphan"
    )
