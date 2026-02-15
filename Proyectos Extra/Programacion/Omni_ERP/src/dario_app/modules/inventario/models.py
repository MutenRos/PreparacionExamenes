"""Inventario (Inventory) models."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Proveedor(Base):
    """Supplier model for purchase orders and automation."""

    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    contacto_nombre: Mapped[str] = mapped_column(String(100), nullable=True)
    direccion: Mapped[str] = mapped_column(Text, nullable=True)
    terminos_pago: Mapped[str] = mapped_column(String(100), nullable=True, default="30 días")
    descuento_volumen: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=True, default=0)
    dias_entrega_promedio: Mapped[int] = mapped_column(Integer, nullable=True, default=7)
    es_activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    documento_proveedor: Mapped[str] = mapped_column(String(50), nullable=True)  # RUC, NIF, etc.
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Producto(Base):
    """Product model for inventory management.
    
    Gestiona productos del inventario incluyendo precios, stock,
    ubicación en almacén y relación con proveedores.
    """

    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    categoria: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    precio_compra: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    precio_venta: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    margen_porcentaje: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=True, default=20
    )  # % de ganancia
    stock_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stock_minimo: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cantidad_minima_compra: Mapped[int] = mapped_column(
        Integer, nullable=True, default=1
    )  # Para auto-compra
    unidad_medida: Mapped[str] = mapped_column(String(20), nullable=False, default="unidad")
    ubicacion_almacen: Mapped[str | None] = mapped_column(String(100), nullable=True)
    proveedor_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("proveedores.id"), nullable=True
    )
    precio_ultima_compra: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    visible_en_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    es_alquiler: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
