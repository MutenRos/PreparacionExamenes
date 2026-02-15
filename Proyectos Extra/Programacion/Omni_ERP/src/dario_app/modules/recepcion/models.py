"""Models for purchase receipt and internal logistics."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class EstadoAlbaran(str, Enum):
    """States for internal receipts (albaranes)."""
    PENDIENTE = "pendiente"          # Receipt awaiting items
    PARCIAL = "parcial"              # Partially received
    COMPLETO = "completo"            # Fully received
    VERIFICADO = "verificado"        # Verified against invoice
    CANCELADO = "cancelado"          # Cancelled


class UbicacionAlmacen(str, Enum):
    """Storage locations in warehouse."""
    PLAYA_ENTRADA = "playa_entrada"  # Entry dock
    PICKING = "picking"              # Picking zone (for current production)
    ALMACEN = "almacen"              # Main storage


class EstadoMovimiento(str, Enum):
    """States for logistics movements."""
    PENDIENTE = "pendiente"          # Movement waiting to start
    EN_TRANSITO = "en_transito"      # In movement
    EN_PICKING = "en_picking"        # At picking location (being picked)
    COMPLETADO = "completado"        # Movement completed
    CANCELADO = "cancelado"          # Cancelled


class Albaran(Base):
    """Internal receipt document (albarán) for purchase orders."""

    __tablename__ = "albaranes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    numero: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    compra_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("compras.id"), nullable=False, index=True
    )
    
    # Receipt details
    fecha_recepcion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    usuario_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=True
    )
    
    # Status
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default=EstadoAlbaran.PENDIENTE.value)
    
    # Tracking
    total_items: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    items_recibidos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # For later invoice reconciliation
    numero_factura_externa: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fecha_factura_externa: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    diferencias_observadas: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class AlbaranDetalle(Base):
    """Individual items in a receipt (albarán)."""

    __tablename__ = "albaranes_detalle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    albaran_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("albaranes.id"), nullable=False, index=True
    )
    compra_detalle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("compras_detalle.id"), nullable=False, index=True
    )
    producto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("productos.id"), nullable=False, index=True
    )
    
    # Quantities
    cantidad_ordenada: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad_recibida: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cantidad_diferencia: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Quality check
    lotes_recibidos: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Batch numbers
    fechas_vencimiento: Mapped[str | None] = mapped_column(String(500), nullable=True)
    inspecciono: Mapped[str | None] = mapped_column(String(100), nullable=True)  # Inspector name
    
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MovimientoLogistico(Base):
    """Internal logistics movement order."""

    __tablename__ = "movimientos_logisticos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    numero: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    
    # Related to receipt
    albaran_detalle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("albaranes_detalle.id"), nullable=False, index=True
    )
    producto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("productos.id"), nullable=False, index=True
    )
    
    # Related to production order if applicable
    orden_produccion_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ordenes_produccion.id"), nullable=True
    )
    seccion_produccion: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Movement details
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    ubicacion_origen: Mapped[str] = mapped_column(
        String(50), nullable=False, default=UbicacionAlmacen.PLAYA_ENTRADA.value
    )
    ubicacion_destino: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Assignment
    carretillero_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=True
    )
    
    # Status
    estado: Mapped[str] = mapped_column(
        String(20), nullable=False, default=EstadoMovimiento.PENDIENTE.value
    )
    
    # Tracking
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_inicio: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_completado: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class FacturaExterna(Base):
    """External supplier invoices for reconciliation."""

    __tablename__ = "facturas_externas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    numero: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    albaran_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("albaranes.id"), nullable=True
    )
    compra_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("compras.id"), nullable=False, index=True
    )
    
    # Invoice details
    proveedor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("proveedores.id"), nullable=False, index=True
    )
    fecha_emision: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    monto_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Reconciliation
    estado_reconciliacion: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pendiente"  # pendiente, parcial, completa, diferencias
    )
    diferencia_cantidad: Mapped[str | None] = mapped_column(Text, nullable=True)
    diferencia_precio: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    
    fecha_recibido: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
