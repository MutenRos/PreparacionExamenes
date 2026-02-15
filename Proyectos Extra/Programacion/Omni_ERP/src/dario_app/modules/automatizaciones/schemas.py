"""Schemas para API de automatizaciones."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from dario_app.modules.automatizaciones.models import (
    TipoTrigger,
    TipoAccion,
    EstadoAutomatizacion,
)


class CondicionSchema(BaseModel):
    """Schema para condiciones."""
    campo: str = Field(..., description="Campo a evaluar (ej: monto)")
    operador: str = Field(..., description="Operador (=, >, <, contains, etc)")
    valor: str = Field(..., description="Valor esperado")


class AccionSchema(BaseModel):
    """Schema para una acción."""
    tipo_accion: TipoAccion
    parametros: Dict[str, Any] = Field(..., description="Parámetros de la acción")
    orden: int = 0
    activa: bool = True


class AutomatizacionCreateSchema(BaseModel):
    """Schema para crear automatización."""
    nombre: str = Field(..., min_length=3, max_length=255)
    descripcion: Optional[str] = None
    tipo_trigger: TipoTrigger
    condiciones: Optional[Dict[str, Any]] = None
    acciones: List[AccionSchema] = Field(..., min_items=1)
    continuar_en_error: bool = False
    tiempo_espera_minutos: int = 0


class AutomatizacionUpdateSchema(BaseModel):
    """Schema para actualizar automatización."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[EstadoAutomatizacion] = None
    activa: Optional[bool] = None
    condiciones: Optional[Dict[str, Any]] = None
    acciones: Optional[List[AccionSchema]] = None
    continuar_en_error: Optional[bool] = None
    tiempo_espera_minutos: Optional[int] = None


class AutomatizacionResponseSchema(BaseModel):
    """Schema para respuesta de automatización."""
    id: int
    organization_id: int
    nombre: str
    descripcion: Optional[str]
    tipo_trigger: TipoTrigger
    estado: EstadoAutomatizacion
    activa: bool
    condiciones: Optional[Dict[str, Any]]
    acciones: List[AccionSchema]
    
    total_ejecuciones: int = 0
    ejecuciones_exitosas: int = 0
    ejecuciones_fallidas: int = 0
    ultima_ejecucion: Optional[datetime] = None
    
    creado_en: datetime
    actualizado_en: datetime
    creado_por: Optional[int] = None
    
    class Config:
        from_attributes = True


class RegistroAutomatizacionResponseSchema(BaseModel):
    """Schema para registro de ejecución."""
    id: int
    automatizacion_id: int
    resultado: str  # "exito" o "error"
    mensaje_error: Optional[str]
    acciones_ejecutadas: Optional[Dict[str, Any]]
    ejecutado_en: datetime
    
    class Config:
        from_attributes = True


class TemplateAutomatizacionSchema(BaseModel):
    """Template predefinido de automatización."""
    nombre: str
    descripcion: str
    tipo_trigger: TipoTrigger
    acciones: List[AccionSchema]
    condiciones: Optional[Dict[str, Any]] = None


# Templates predefinidos
TEMPLATES_AUTOMATIZACIONES = {
    "notificacion_venta": TemplateAutomatizacionSchema(
        nombre="Notificar venta nueva",
        descripcion="Envía email y WhatsApp cuando se crea una venta",
        tipo_trigger=TipoTrigger.VENTA_CREADA,
        acciones=[
            AccionSchema(
                tipo_accion=TipoAccion.ENVIAR_EMAIL_CLIENTE,
                parametros={
                    "asunto": "¡Hemos recibido tu venta!",
                    "cuerpo": "Gracias por comprar con nosotros. Tu orden es: {{venta.numero}}"
                },
                orden=1
            ),
            AccionSchema(
                tipo_accion=TipoAccion.CREAR_EVENTO_CALENDARIO,
                parametros={
                    "titulo": "Venta: {{venta.numero}}",
                    "descripcion": "Monto: {{venta.monto}}",
                    "fecha_inicio": "{{venta.fecha}}",
                    "tipo": "venta"
                },
                orden=2
            )
        ]
    ),
    
    "alerta_stock_bajo": TemplateAutomatizacionSchema(
        nombre="Alerta de stock bajo",
        descripcion="Genera orden de compra cuando el stock baja del mínimo",
        tipo_trigger=TipoTrigger.STOCK_BAJO,
        acciones=[
            AccionSchema(
                tipo_accion=TipoAccion.GENERAR_ORDEN_COMPRA,
                parametros={
                    "producto_id": "{{producto.id}}",
                    "cantidad": "{{producto.stock_minimo_ordenar}}"
                },
                orden=1
            ),
            AccionSchema(
                tipo_accion=TipoAccion.CREAR_TAREA,
                parametros={
                    "titulo": "Revisar compra: {{producto.nombre}}",
                    "descripcion": "Stock bajo - se generó orden automáticamente"
                },
                orden=2
            )
        ]
    ),
    
    "recordatorio_pago": TemplateAutomatizacionSchema(
        nombre="Recordatorio de pago atrasado",
        descripcion="Envía recordatorio cuando un pago está atrasado",
        tipo_trigger=TipoTrigger.PAGO_ATRASADO,
        acciones=[
            AccionSchema(
                tipo_accion=TipoAccion.ENVIAR_EMAIL_CLIENTE,
                parametros={
                    "asunto": "Recordatorio: Pago pendiente",
                    "cuerpo": "Tu factura {{venta.numero}} vence el {{venta.fecha_vencimiento}}. Monto: {{venta.monto}}"
                },
                orden=1
            )
        ]
    ),
    
    "confirmacion_cita": TemplateAutomatizacionSchema(
        nombre="Confirmación automática de cita",
        descripcion="Envía confirmación cuando se crea una cita",
        tipo_trigger=TipoTrigger.CITA_CREADA,
        acciones=[
            AccionSchema(
                tipo_accion=TipoAccion.ENVIAR_EMAIL_CLIENTE,
                parametros={
                    "asunto": "Cita confirmada",
                    "cuerpo": "Tu cita está programada para {{cita.fecha_hora}}"
                },
                orden=1
            )
        ]
    )
}
