"""Ventas (Sales) models."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Venta(Base):
    """Sales order model."""

    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    numero: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Client info (Spain tax compliance)
    cliente_nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    cliente_nif_nie: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    cliente_email: Mapped[str] = mapped_column(String(200), nullable=True)
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey("clientes.id"), nullable=True)

    # Client fiscal address
    cliente_domicilio: Mapped[str | None] = mapped_column(Text, nullable=True)
    cliente_municipio: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cliente_provincia: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cliente_codigo_postal: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Sale amounts
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    base_imponible: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    iva: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    irpf: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)  # Retención IRPF si aplica
    porcentaje_iva: Mapped[int] = mapped_column(Integer, default=21)  # 21%, 10%, 4%

    # Invoice tracking
    factura_generada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    factura_numero: Mapped[str] = mapped_column(String(50), nullable=True)
    factura_enviada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    template_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("document_templates.id"), nullable=True
    )

    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="pendiente")
    notas: Mapped[str] = mapped_column(Text, nullable=True)

    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class VentaDetalle(Base):
    """Sales order line items."""

    __tablename__ = "ventas_detalle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    venta_id: Mapped[int] = mapped_column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
