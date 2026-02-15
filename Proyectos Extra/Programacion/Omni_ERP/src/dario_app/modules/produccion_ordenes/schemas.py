"""Pydantic schemas for production orders."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from .models import EstadoOrdenProduccion, TipoPrioridad, TipoSeccion


# ============ OPERACIÓN PRODUCCIÓN ============

class OperacionProduccionBase(BaseModel):
    """Base operación schema."""
    bom_operacion_id: int
    secuencia: int = 10
    duracion_estimada: Optional[float] = None
    asignado_a: Optional[str] = None
    centro_trabajo: Optional[str] = None


class OperacionProduccionCreate(OperacionProduccionBase):
    """Create operación request."""
    pass


class OperacionProduccionUpdate(BaseModel):
    """Update operación request."""
    estado: Optional[EstadoOrdenProduccion] = None
    duracion_real: Optional[float] = None
    asignado_a: Optional[str] = None
    centro_trabajo: Optional[str] = None
    fecha_inicio_real: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    inspecciones_realizadas: Optional[bool] = None
    resultado_control_calidad: Optional[str] = None
    comentarios_qc: Optional[str] = None
    defectos_encontrados: Optional[str] = None
    acciones_correctivas: Optional[str] = None


class OperacionProduccionResponse(OperacionProduccionBase):
    """Operación response."""
    id: int
    orden_produccion_id: int
    estado: EstadoOrdenProduccion
    fecha_inicio_estimada: Optional[datetime]
    fecha_fin_estimada: Optional[datetime]
    fecha_inicio_real: Optional[datetime]
    fecha_fin_real: Optional[datetime]
    duracion_real: Optional[float]
    inspecciones_realizadas: bool
    resultado_control_calidad: Optional[str]

    class Config:
        from_attributes = True


# ============ MOVIMIENTO ALMACÉN ============

class MovimientoAlmacenBase(BaseModel):
    """Base movimiento schema."""
    producto_id: int
    tipo_movimiento: str
    cantidad: float
    ubicacion_origen: Optional[str] = None
    ubicacion_destino: Optional[str] = None


class MovimientoAlmacenCreate(MovimientoAlmacenBase):
    """Create movimiento request."""
    pass


class MovimientoAlmacenUpdate(BaseModel):
    """Update movimiento request."""
    estado: Optional[str] = None
    usuario_asignado_id: Optional[int] = None
    fecha_movimiento: Optional[datetime] = None
    responsable: Optional[str] = None
    observaciones: Optional[str] = None


class MovimientoAlmacenResponse(MovimientoAlmacenBase):
    """Movimiento response."""
    id: int
    orden_produccion_id: int
    usuario_asignado_id: Optional[int] = None
    estado: str
    fecha_creacion: datetime
    fecha_asignacion: Optional[datetime] = None
    fecha_movimiento: Optional[datetime]
    responsable: Optional[str]
    observaciones: Optional[str]
    producto_codigo: Optional[str] = None
    producto_nombre: Optional[str] = None

    class Config:
        from_attributes = True


# ============ ORDEN PRODUCCIÓN ============

class OrdenProduccionBase(BaseModel):
    """Base orden producción schema."""
    venta_id: int
    bom_id: int
    producto_id: int
    cantidad_ordenada: float = 1.0
    descripcion: Optional[str] = None
    prioridad: TipoPrioridad = TipoPrioridad.MEDIA
    carretillero_id: Optional[int] = None


class OrdenProduccionCreate(OrdenProduccionBase):
    """Create orden producción request."""
    pass


class OrdenProduccionUpdate(BaseModel):
    """Update orden producción request."""
    estado: Optional[EstadoOrdenProduccion] = None
    cantidad_completada: Optional[float] = None
    cantidad_rechazada: Optional[float] = None
    asignado_a: Optional[str] = None
    centro_trabajo: Optional[str] = None
    fecha_inicio_real: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    notas_produccion: Optional[str] = None
    prioridad: Optional[TipoPrioridad] = None
    costo_materiales: Optional[Decimal] = None
    costo_mano_obra: Optional[Decimal] = None
    costo_operaciones_externas: Optional[Decimal] = None
    carretillero_id: Optional[int] = None


class OrdenProduccionStateChange(BaseModel):
    """Change production order state."""
    nuevo_estado: EstadoOrdenProduccion
    notas: Optional[str] = None


class OrdenProduccionResponse(OrdenProduccionBase):
    """Orden producción response."""
    id: int
    numero: str
    estado: EstadoOrdenProduccion
    cantidad_completada: float
    cantidad_rechazada: float
    fecha_creacion: datetime
    fecha_inicio_estimada: Optional[datetime]
    fecha_fin_estimada: Optional[datetime]
    fecha_inicio_real: Optional[datetime]
    fecha_fin_real: Optional[datetime]
    asignado_a: Optional[str]
    centro_trabajo: Optional[str]
    carretillero_id: Optional[int] = None
    costo_materiales: Decimal
    costo_mano_obra: Decimal
    costo_operaciones_externas: Decimal
    costo_total: Decimal
    venta_numero: Optional[str] = None
    cliente_nombre: Optional[str] = None
    operaciones: List[OperacionProduccionResponse] = []

    class Config:
        from_attributes = True


class OrdenProduccionDetailResponse(OrdenProduccionResponse):
    """Detailed orden producción response."""
    movimientos_material: List[MovimientoAlmacenResponse] = []

    class Config:
        from_attributes = True


# ============ BULK ACTIONS ============

class BulkPrioridadRequest(BaseModel):
    """Bulk priority update request."""
    prioridad: TipoPrioridad
    ids: List[int]


class OrdenProduccionListResponse(BaseModel):
    """List response for production orders."""
    id: int
    numero: str
    venta_id: int
    venta_numero: Optional[str] = None
    cliente_nombre: Optional[str] = None
    producto_id: int
    cantidad_ordenada: float
    cantidad_completada: float
    estado: EstadoOrdenProduccion
    prioridad: TipoPrioridad
    fecha_creacion: datetime
    fecha_fin_estimada: Optional[datetime]
    asignado_a: Optional[str]
    carretillero_id: Optional[int] = None
    carretillero_nombre: Optional[str] = None
    seccion_produccion_id: Optional[int] = None
    seccion_produccion_nombre: Optional[str] = None
    fecha_asignacion: Optional[datetime] = None
    fecha_aceptacion: Optional[datetime] = None
    movimientos_material: Optional[List] = None

    class Config:
        from_attributes = True


# ============ SECCIÓN PRODUCCIÓN ============

class SeccionProduccionBase(BaseModel):
    """Base sección producción schema."""
    codigo: Optional[str] = None  # Se autogenera cuando no se envía
    nombre: str
    descripcion: Optional[str] = None
    tipo: TipoSeccion = TipoSeccion.OTRO
    capacidad_diaria: Optional[float] = None
    capacidad_operarios: Optional[int] = None
    supervisor_id: Optional[int] = None
    supervisor_nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    zona_picking: Optional[str] = None
    activa: bool = True


class SeccionProduccionCreate(SeccionProduccionBase):
    """Create sección request."""
    pass


class SeccionProduccionUpdate(BaseModel):
    """Update sección request."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[TipoSeccion] = None
    capacidad_diaria: Optional[float] = None
    capacidad_operarios: Optional[int] = None
    supervisor_id: Optional[int] = None
    supervisor_nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    activa: Optional[bool] = None
    notas: Optional[str] = None


class SeccionProduccionResponse(SeccionProduccionBase):
    """Sección response."""
    id: int
    organization_id: int
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime]
    notas: Optional[str]
    ordenes_activas: int = 0  # Computed field

    class Config:
        from_attributes = True


# ============ WORKFLOW ACTIONS ============

class AsignarSeccionRequest(BaseModel):
    """Request to assign order to production section."""
    seccion_produccion_id: int
    asignado_a: Optional[str] = None
    notas: Optional[str] = None


class AceptarOrdenRequest(BaseModel):
    """Request for supervisor to accept order."""
    notas: Optional[str] = None
