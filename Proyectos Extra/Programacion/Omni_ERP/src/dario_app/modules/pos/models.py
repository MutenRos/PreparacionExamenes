"""Point of Sale (POS) models."""

from datetime import datetime
import secrets

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dario_app.database import Base


class VentaPOS(Base):
    """Point of Sale transaction."""

    __tablename__ = "ventas_pos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    numero: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey("clientes.id"), nullable=True)

    # Payment
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    descuento: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    impuesto: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    metodo_pago: Mapped[str] = mapped_column(String(50), nullable=False, default="efectivo")
    monto_pagado: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    cambio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    # Status
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="completada")

    # Observaciones del comercial
    observaciones: Mapped[str] = mapped_column(Text, nullable=True)

    # Timestamps
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    detalles = relationship("VentaPOSDetalle", back_populates="venta", cascade="all, delete-orphan")


class VentaPOSDetalle(Base):
    """POS transaction line items."""

    __tablename__ = "ventas_pos_detalle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    venta_pos_id: Mapped[int] = mapped_column(Integer, ForeignKey("ventas_pos.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey("productos.id"), nullable=False)

    cantidad: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    precio_unitario: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    descuento: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Relationships
    venta = relationship("VentaPOS", back_populates="detalles")


class PosWidget(Base):
    """POS Widget for embedding in external websites (PRO feature)."""

    __tablename__ = "pos_widgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Widget identification
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    # Widget configuration
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    url_permitida: Mapped[str] = mapped_column(String(500), nullable=False)  # Domain where widget is embedded
    
    # Styling
    color_primario: Mapped[str] = mapped_column(String(7), nullable=False, default="#2563eb")
    color_boton: Mapped[str] = mapped_column(String(7), nullable=False, default="#10b981")
    icono_carrito: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    mostrar_precio: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    mostrar_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Filtering
    categorias_ids: Mapped[str] = mapped_column(String(500), nullable=True)  # JSON array as string
    productos_ids: Mapped[str] = mapped_column(String(1000), nullable=True)  # JSON array as string
    solo_disponibles: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Status
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

