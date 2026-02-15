"""Schemas para el módulo de calendario."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EventoBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    tipo: str = Field(..., description="compra, venta, recordatorio, reunion, deadline")
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    todo_el_dia: bool = False
    venta_id: Optional[int] = None
    compra_id: Optional[int] = None
    producto_id: Optional[int] = None
    cliente_id: Optional[int] = None
    completado: bool = False
    color: str = "#667eea"


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    todo_el_dia: Optional[bool] = None
    completado: Optional[bool] = None
    color: Optional[str] = None


class EventoResponse(EventoBase):
    id: int
    organization_id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True
