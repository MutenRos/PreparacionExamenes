"""Production module models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrdenInternal(BaseModel):
    """Internal production order."""
    id: str
    numero: str
    producto: str
    seccion_produccion: Optional[str] = None  # ID de la sección de producción asignada
    etapa: str
    avance: int  # percentage 0-100
    estado: str  # "picking", "en_curso", "demora", "completada"
    fecha_inicio: datetime
    fecha_prevista: datetime
    responsable: Optional[str] = None


class OrdenExterna(BaseModel):
    """External production order (third-party)."""
    id: str
    numero: str
    proveedor: str
    estado: str  # "pendiente", "en_transito", "en_proceso", "devuelto"
    fecha_envio: datetime
    eta: Optional[datetime] = None
    notas: Optional[str] = None


class Alerta(BaseModel):
    """Production alert."""
    id: str
    orden: str
    motivo: str
    severidad: str  # "baja", "media", "alta"
    fecha: datetime


class EstadisticasProduccion(BaseModel):
    """Production statistics."""
    ordenes_activas: int
    ordenes_internas: int
    ordenes_externas: int
    cumplimiento_vs_plan: float  # percentage
