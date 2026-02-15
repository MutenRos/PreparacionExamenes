"""Compras (Purchases) models."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Compra(Base):
    """Purchase order model."""

    __tablename__ = "compras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    numero: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    proveedor_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("proveedores.id"), nullable=True
    )
    proveedor_nombre: Mapped[str] = mapped_column(
        String(200), nullable=False
    )  # Fallback si no tiene FK
    proveedor_documento: Mapped[str] = mapped_column(String(50), nullable=True)
    proveedor_email: Mapped[str] = mapped_column(String(150), nullable=True)  # Para envío de email
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="pendiente")
    
    # Recepción de compra
    estado_recepcion: Mapped[str] = mapped_column(
        String(20), nullable=False, default="no_recibida"
    )  # no_recibida, parcial, completa
    cantidad_items_esperados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cantidad_items_recibidos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    fecha_primera_recepcion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class CompraDetalle(Base):
    """Purchase order line items."""

    __tablename__ = "compras_detalle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    compra_id: Mapped[int] = mapped_column(Integer, ForeignKey("compras.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
