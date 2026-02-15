"""Models for production orders management."""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from dario_app.database import Base
import enum


class EstadoOrdenProduccion(str, enum.Enum):
    """Production order states - full workflow."""
    PLANIFICADA = "planificada"  # Created/planned but not yet in assignment flow
    PENDIENTE_ASIGNACION = "pendiente_asignacion"  # Created, waiting section assignment
    ASIGNADA = "asignada"  # Assigned to production section
    ACEPTADA = "aceptada"  # Accepted by supervisor
    ADQUISICION_MATERIALES = "adquisicion_materiales"  # Materials being prepared
    EN_PROCESO = "en_proceso"  # In production
    PAUSADA = "pausada"  # Paused
    COMPLETADA = "completada"  # Finished
    CANCELADA = "cancelada"  # Cancelled


class TipoPrioridad(str, enum.Enum):
    """Priority levels."""
    MUY_BAJA = "muy_baja"
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class OrdenProduccion(Base):
    """Production order - generated from a sales order."""
    
    __tablename__ = "ordenes_produccion"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Links to sales and BOM
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False, index=True)
    bom_id = Column(Integer, ForeignKey("bom_headers.id"), nullable=False, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False, index=True)
    
    # Order info
    numero = Column(String(50), unique=True, nullable=False, index=True)  # e.g., "OP-2025-001"
    descripcion = Column(String(500))
    
    # Quantities
    cantidad_ordenada = Column(Float, nullable=False, default=1.0)
    cantidad_completada = Column(Float, default=0.0)
    cantidad_rechazada = Column(Float, default=0.0)
    
    # Status and priority
    estado = Column(String(50), default=EstadoOrdenProduccion.PENDIENTE_ASIGNACION.value, nullable=False)
    prioridad = Column(String(50), default=TipoPrioridad.MEDIA.value)
    
    # Dates
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_inicio_estimada = Column(DateTime)
    fecha_fin_estimada = Column(DateTime)
    fecha_inicio_real = Column(DateTime)
    fecha_fin_real = Column(DateTime)
    
    # Assignment
    seccion_produccion_id = Column(Integer, ForeignKey("secciones_produccion.id"), index=True)
    asignado_a = Column(String(100))  # Supervisor/responsible person
    centro_trabajo = Column(String(100))  # Production line
    fecha_asignacion = Column(DateTime)  # When assigned to section
    fecha_aceptacion = Column(DateTime)  # When supervisor accepted
    carretillero_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    
    # Cost tracking
    costo_materiales = Column(Numeric(10, 2), default=0)
    costo_mano_obra = Column(Numeric(10, 2), default=0)
    costo_operaciones_externas = Column(Numeric(10, 2), default=0)
    costo_total = Column(Numeric(10, 2), default=0)
    
    # Notes
    notas_produccion = Column(Text)
    notas_internas = Column(Text)
    
    # Relationships
    venta = relationship("Venta", foreign_keys=[venta_id])
    bom = relationship("BOMHeader", foreign_keys=[bom_id])
    producto = relationship("Producto", foreign_keys=[producto_id])
    seccion_produccion = relationship("SeccionProduccion", foreign_keys=[seccion_produccion_id], back_populates="ordenes")
    operaciones = relationship("OperacionProduccion", back_populates="orden", cascade="all, delete-orphan")
    movimientos_material = relationship("MovimientoAlmacen", back_populates="orden_produccion")
    carretillero = relationship("Usuario")


class OperacionProduccion(Base):
    """Production operations within an order."""
    
    __tablename__ = "operaciones_produccion"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    orden_produccion_id = Column(Integer, ForeignKey("ordenes_produccion.id"), nullable=False, index=True)
    bom_operacion_id = Column(Integer, ForeignKey("bom_operaciones.id"), nullable=False, index=True)
    
    # Sequence and timing
    secuencia = Column(Integer, default=10)
    duracion_estimada = Column(Float)  # hours
    duracion_real = Column(Float)  # hours (recorded after completion)
    
    # Status (use order workflow states; default to pendiente_asignacion for alignment)
    estado = Column(String(50), default=EstadoOrdenProduccion.PENDIENTE_ASIGNACION.value)
    
    # Assignment
    asignado_a = Column(String(100))
    centro_trabajo = Column(String(100))
    
    # Dates
    fecha_inicio_estimada = Column(DateTime)
    fecha_fin_estimada = Column(DateTime)
    fecha_inicio_real = Column(DateTime)
    fecha_fin_real = Column(DateTime)
    
    # Quality control
    inspecciones_realizadas = Column(Boolean, default=False)
    resultado_control_calidad = Column(String(50))  # aprobado, rechazado, con_observaciones
    comentarios_qc = Column(Text)
    
    # Defects tracking
    defectos_encontrados = Column(Text)
    acciones_correctivas = Column(Text)
    
    # Relationships
    orden = relationship("OrdenProduccion", back_populates="operaciones")
    bom_operacion = relationship("BOMOperacion")


class MovimientoAlmacen(Base):
    """Material movements from warehouse to production."""
    
    __tablename__ = "movimientos_almacen"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # References
    orden_produccion_id = Column(Integer, ForeignKey("ordenes_produccion.id"), nullable=False, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False, index=True)
    usuario_asignado_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)  # Forklift operator/carretillero
    
    # Movement details
    tipo_movimiento = Column(String(50), nullable=False)  # picking, devolución, reposición
    cantidad = Column(Float, nullable=False)
    
    # Locations
    ubicacion_origen = Column(String(100))  # Rack/aisle in warehouse
    ubicacion_destino = Column(String(100))  # Production line or section
    
    # Status
    estado = Column(String(50), default="pendiente")  # pendiente, en_transito, entregado, rechazado
    
    # Tracking
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_asignacion = Column(DateTime, nullable=True)
    fecha_movimiento = Column(DateTime)
    responsable = Column(String(100))
    
    # Notes
    observaciones = Column(Text)
    
    # Relationships
    orden_produccion = relationship("OrdenProduccion", back_populates="movimientos_material")
    producto = relationship("Producto")
    usuario_asignado = relationship("Usuario")


class TipoSeccion(str, enum.Enum):
    """Production section types."""
    CORTE = "corte"
    MECANIZADO = "mecanizado"
    ENSAMBLAJE = "ensamblaje"
    SOLDADURA = "soldadura"
    PINTURA = "pintura"
    ACABADO = "acabado"
    CONTROL_CALIDAD = "control_calidad"
    EMPAQUE = "empaque"
    OTRO = "otro"


class SeccionProduccion(Base):
    """Production sections/departments where work is performed."""
    
    __tablename__ = "secciones_produccion"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Section info
    codigo = Column(String(50), unique=True, nullable=False, index=True)  # e.g., "SEC-CORTE-01"
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    tipo = Column(String(50), default="otro")  # Enum values: corte, mecanizado, ensamblaje, soldadura, pintura, acabado, control_calidad, empaque, otro
    
    # Capacity
    capacidad_diaria = Column(Float)  # Units or hours per day
    capacidad_operarios = Column(Integer)  # Max workers
    
    # Assignment
    supervisor_id = Column(Integer, ForeignKey("usuarios.id"), index=True)
    supervisor_nombre = Column(String(100))
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Location
    ubicacion = Column(String(200))  # Building, floor, area
    zona_picking = Column(String(200))  # Staging/picking zone for material kitting
    
    # Metadata
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, onupdate=datetime.utcnow)
    notas = Column(Text)
    
    # Relationships
    ordenes = relationship("OrdenProduccion", back_populates="seccion_produccion")


class RegistroTrabajo(Base):
    """Simple work log entries for a production order."""

    __tablename__ = "registro_trabajo"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    orden_produccion_id = Column(Integer, ForeignKey("ordenes_produccion.id"), nullable=False, index=True)
    trabajador_nombre = Column(String(100), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    hora_inicio = Column(String(20), nullable=False)
    hora_fin = Column(String(20))
    notas = Column(Text)

    orden = relationship("OrdenProduccion")


class IncidenciaProduccion(Base):
    """Incidents reported against a production order."""

    __tablename__ = "incidencias_produccion"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    orden_produccion_id = Column(Integer, ForeignKey("ordenes_produccion.id"), nullable=False, index=True)
    tipo_incidencia = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_reporte = Column(DateTime, default=datetime.utcnow, nullable=False)
    estado = Column(String(50), default="reportada")

    orden = relationship("OrdenProduccion")


class SolicitudMaterialProduccion(Base):
    """Material requests tied to a production order."""

    __tablename__ = "solicitudes_material_produccion"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    orden_produccion_id = Column(Integer, ForeignKey("ordenes_produccion.id"), nullable=False, index=True)
    producto_descripcion = Column(String(200), nullable=False)
    cantidad = Column(Float, nullable=False)
    urgencia = Column(String(50), default="media")
    motivo = Column(Text)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow, nullable=False)
    estado = Column(String(50), default="pendiente")
    observaciones = Column(Text)

    orden = relationship("OrdenProduccion")
