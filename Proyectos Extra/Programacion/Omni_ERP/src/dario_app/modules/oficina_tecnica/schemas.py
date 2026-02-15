"""Pydantic schemas for Oficina Técnica module."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BOMLineBase(BaseModel):
    """Base schema for BOM Line."""
    componente_id: int
    cantidad: float
    unidad_medida: str = "unidad"
    secuencia: int = 10
    es_opcional: bool = False
    notas: Optional[str] = None
    factor_desperdicio: float = 0.0


class BOMLineCreate(BOMLineBase):
    """Schema for creating BOM Line."""
    pass


class BOMLineResponse(BOMLineBase):
    """Schema for BOM Line response."""
    id: int
    bom_header_id: int
    organization_id: int
    componente_nombre: Optional[str] = None
    componente_codigo: Optional[str] = None

    class Config:
        from_attributes = True


class BOMOperacionBase(BaseModel):
    """Base schema for BOM Operation."""
    nombre: str
    codigo: Optional[str] = None
    tipo_operacion: str
    secuencia: int = 10
    duracion_estimada: Optional[float] = None
    centro_trabajo: Optional[str] = None
    proveedor_id: Optional[int] = None
    costo_operacion: float = 0.0
    descripcion: Optional[str] = None
    instrucciones: Optional[str] = None


class BOMOperacionCreate(BOMOperacionBase):
    """Schema for creating BOM Operation."""
    pass


class BOMOperacionResponse(BOMOperacionBase):
    """Schema for BOM Operation response."""
    id: int
    bom_header_id: int
    organization_id: int
    proveedor_nombre: Optional[str] = None

    class Config:
        from_attributes = True


class BOMHeaderBase(BaseModel):
    """Base schema for BOM Header."""
    producto_id: int
    nombre: str
    codigo: str
    version: str = "1.0"
    cantidad_producida: float = 1.0
    unidad_medida: str = "unidad"
    descripcion: Optional[str] = None
    notas_tecnicas: Optional[str] = None
    activo: bool = True
    es_principal: bool = True


class BOMHeaderCreate(BOMHeaderBase):
    """Schema for creating BOM Header with lines and operations."""
    lineas: List[BOMLineCreate] = []
    operaciones: List[BOMOperacionCreate] = []


class BOMHeaderUpdate(BaseModel):
    """Schema for updating BOM Header."""
    nombre: Optional[str] = None
    version: Optional[str] = None
    descripcion: Optional[str] = None
    notas_tecnicas: Optional[str] = None
    activo: Optional[bool] = None
    es_principal: Optional[bool] = None


class BOMHeaderResponse(BOMHeaderBase):
    """Schema for BOM Header response."""
    id: int
    organization_id: int
    producto_nombre: Optional[str] = None
    producto_codigo: Optional[str] = None
    lineas: List[BOMLineResponse] = []
    operaciones: List[BOMOperacionResponse] = []

    class Config:
        from_attributes = True


class BOMSummary(BaseModel):
    """Summary of a BOM for list views."""
    id: int
    codigo: str
    nombre: str
    producto_nombre: str
    version: str
    activo: bool
    total_componentes: int
    total_operaciones: int

    class Config:
        from_attributes = True
