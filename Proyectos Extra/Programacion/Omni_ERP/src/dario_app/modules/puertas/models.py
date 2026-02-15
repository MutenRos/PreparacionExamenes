"""Puertas (Doors) models for warehouse entry/exit points."""

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class TipoPuerta(str, Enum):
    """Door type enumeration."""
    ENTRADA = "entrada"
    SALIDA = "salida"


class Puerta(Base):
    """Door model for warehouse entry/exit points."""

    __tablename__ = "puertas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(
        SQLEnum(TipoPuerta), nullable=False, default=TipoPuerta.ENTRADA
    )
    ubicacion: Mapped[str] = mapped_column(String(200), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    responsable_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=True, index=True
    )
    responsable_nombre: Mapped[str] = mapped_column(String(100), nullable=True)
    es_activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    requiere_autorizacion: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    horario_apertura: Mapped[str] = mapped_column(String(10), nullable=True)  # HH:MM format
    horario_cierre: Mapped[str] = mapped_column(String(10), nullable=True)    # HH:MM format
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class MovimientoPuerta(Base):
    """Movement record for door entry/exit tracking."""

    __tablename__ = "movimientos_puertas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    puerta_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("puertas.id"), nullable=False, index=True
    )
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=True, index=True
    )
    usuario_nombre: Mapped[str] = mapped_column(String(100), nullable=True)
    referencia_documento: Mapped[str] = mapped_column(String(50), nullable=True, index=True)
    tipo_documento: Mapped[str] = mapped_column(String(50), nullable=True)  # orden_compra, orden_venta, etc.
    documento_id: Mapped[int] = mapped_column(Integer, nullable=True)
    cantidad_items: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    autorizado_por_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=True
    )
    autorizado_por_nombre: Mapped[str] = mapped_column(String(100), nullable=True)
    estado: Mapped[str] = mapped_column(String(50), nullable=False, default="pendiente")  # pendiente, autorizado, completado, rechazado
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completado_en: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class RecepcionDetalle(Base):
    """Detailed tracking of received items per reception."""

    __tablename__ = "recepcion_detalles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    movimiento_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("movimientos_puertas.id"), nullable=False, index=True
    )
    tipo_documento: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    documento_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    producto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("productos.id"), nullable=False, index=True
    )
    cantidad_esperada: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad_recibida: Mapped[int] = mapped_column(Integer, nullable=False)
    estado_recepcion: Mapped[str] = mapped_column(String(50), nullable=False, default="recibido")  # recibido, dañado, rechazado
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
