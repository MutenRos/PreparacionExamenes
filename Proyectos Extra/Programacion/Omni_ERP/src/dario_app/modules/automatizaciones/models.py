"""Modelos para el sistema de automatizaciones."""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from dario_app.database import Base


class TipoTrigger(str, enum.Enum):
    """Tipos de triggers disponibles."""
    VENTA_CREADA = "venta_creada"
    VENTA_COMPLETADA = "venta_completada"
    COMPRA_CREADA = "compra_creada"
    COMPRA_RECIBIDA = "compra_recibida"
    STOCK_BAJO = "stock_bajo"
    CLIENTE_CREADO = "cliente_creado"
    PAGO_RECIBIDO = "pago_recibido"
    PAGO_ATRASADO = "pago_atrasado"
    CITA_CREADA = "cita_creada"
    CITA_CONFIRMADA = "cita_confirmada"
    HORARIO_PROGRAMADO = "horario_programado"  # Ejecutar a hora específica
    EVENTO_PERSONALIZADO = "evento_personalizado"  # Hook personalizado


class TipoAccion(str, enum.Enum):
    """Tipos de acciones que se pueden ejecutar."""
    # Email
    ENVIAR_EMAIL = "enviar_email"
    ENVIAR_EMAIL_CLIENTE = "enviar_email_cliente"
    ENVIAR_EMAIL_PROVEEDOR = "enviar_email_proveedor"
    
    # WhatsApp
    ENVIAR_WHATSAPP = "enviar_whatsapp"
    ENVIAR_WHATSAPP_CLIENTE = "enviar_whatsapp_cliente"
    ENVIAR_WHATSAPP_PROVEEDOR = "enviar_whatsapp_proveedor"
    
    # Crear registros
    CREAR_TAREA = "crear_tarea"
    CREAR_EVENTO_CALENDARIO = "crear_evento_calendario"
    CREAR_NOTIFICACION = "crear_notificacion"
    CREAR_NOTA = "crear_nota"
    
    # Actualizar datos
    ACTUALIZAR_CLIENTE = "actualizar_cliente"
    ACTUALIZAR_PRODUCTO = "actualizar_producto"
    CAMBIAR_ESTADO = "cambiar_estado"  # Cambiar estado de venta, compra, etc.
    
    # Operaciones de inventario
    RESERVAR_STOCK = "reservar_stock"
    GENERAR_ORDEN_COMPRA = "generar_orden_compra"
    AJUSTAR_STOCK = "ajustar_stock"
    
    # Reportes y datos
    GENERAR_REPORTE = "generar_reporte"
    GENERAR_FACTURA = "generar_factura"
    EXPORTAR_DATOS = "exportar_datos"
    
    # Integraciones externas
    WEBHOOK = "webhook"  # POST a URL externa
    
    # Copias de seguridad
    REALIZAR_BACKUP = "realizar_backup"


class EstadoAutomatizacion(str, enum.Enum):
    """Estados de una automatización."""
    ACTIVA = "activa"
    PAUSADA = "pausada"
    DESACTIVADA = "desactivada"
    ERROR = "error"


class Automatizacion(Base):
    """Regla de automatización."""
    __tablename__ = "automatizaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    # Trigger y condiciones
    tipo_trigger = Column(SQLEnum(TipoTrigger), nullable=False)
    condiciones = Column(JSON, nullable=True)  # Condiciones JSON adicionales
    
    # Acciones
    acciones = relationship("Accion", back_populates="automatizacion", cascade="all, delete-orphan")
    
    # Estado
    estado = Column(SQLEnum(EstadoAutomatizacion), default=EstadoAutomatizacion.ACTIVA, nullable=False)
    activa = Column(Boolean, default=True, nullable=False)
    
    # Control
    orden_ejecucion = Column(Integer, default=0)  # Para ejecutar múltiples acciones en orden
    continuar_en_error = Column(Boolean, default=False)  # ¿Continuar si una acción falla?
    tiempo_espera_minutos = Column(Integer, default=0)  # Esperar antes de ejecutar (delay)
    
    # Estadísticas
    total_ejecuciones = Column(Integer, default=0)
    ejecuciones_exitosas = Column(Integer, default=0)
    ejecuciones_fallidas = Column(Integer, default=0)
    ultima_ejecucion = Column(DateTime, nullable=True)
    
    # Auditoría
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    creado_por = Column(Integer, nullable=True)


class Accion(Base):
    """Acción que ejecuta una automatización."""
    __tablename__ = "acciones_automatizacion"
    
    id = Column(Integer, primary_key=True, index=True)
    automatizacion_id = Column(Integer, ForeignKey("automatizaciones.id"), nullable=False, index=True)
    automatizacion = relationship("Automatizacion", back_populates="acciones")
    
    organization_id = Column(Integer, index=True, nullable=False)
    tipo_accion = Column(SQLEnum(TipoAccion), nullable=False)
    
    # Parámetros de la acción (JSON flexible)
    parametros = Column(JSON, nullable=False)  # Ej: {"destinatario": "cliente", "asunto": "...", "cuerpo": "..."}
    
    # Control
    orden = Column(Integer, default=0)
    activa = Column(Boolean, default=True)
    
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)


class RegistroAutomatizacion(Base):
    """Registro de cada ejecución de una automatización."""
    __tablename__ = "registros_automatizacion"
    
    id = Column(Integer, primary_key=True, index=True)
    automatizacion_id = Column(Integer, ForeignKey("automatizaciones.id"), nullable=False, index=True)
    organization_id = Column(Integer, index=True, nullable=False)
    
    # Detalles de la ejecución
    trigger_data = Column(JSON, nullable=True)  # Datos que dispararon el trigger
    resultado = Column(String(20), nullable=False)  # "exito" o "error"
    mensaje_error = Column(Text, nullable=True)
    
    # Acciones ejecutadas
    acciones_ejecutadas = Column(JSON, nullable=True)  # [{"accion_id": 1, "resultado": "exito"}, ...]
    
    # Metadata
    ip_origen = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    ejecutado_en = Column(DateTime, default=datetime.utcnow, nullable=False)


class CondicionAutomatizacion(Base):
    """Condiciones para que se ejecute una automatización."""
    __tablename__ = "condiciones_automatizacion"
    
    id = Column(Integer, primary_key=True, index=True)
    automatizacion_id = Column(Integer, ForeignKey("automatizaciones.id"), nullable=False, index=True)
    organization_id = Column(Integer, index=True, nullable=False)
    
    # Campo a evaluar (ej: "monto > 1000")
    campo = Column(String(255), nullable=False)  # Ej: "monto", "cliente.tipo"
    operador = Column(String(50), nullable=False)  # "=", ">", "<", ">=", "<=", "contains", "in", etc.
    valor = Column(String(500), nullable=False)  # Valor a comparar
    
    # Control
    orden = Column(Integer, default=0)
    
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)
