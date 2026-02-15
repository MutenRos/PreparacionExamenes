"""Modelos para eventos del calendario."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from dario_app.database import Base


class Evento(Base):
    """Eventos del calendario (reuniones, recordatorios, deadlines)."""

    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)

    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=False)  # compra, venta, recordatorio, reunion, deadline
    fecha_inicio = Column(DateTime, nullable=False, index=True)
    fecha_fin = Column(DateTime, nullable=True)
    todo_el_dia = Column(Boolean, default=False)

    # Referencias opcionales a otras entidades
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=True)
    compra_id = Column(Integer, ForeignKey("compras.id"), nullable=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)

    completado = Column(Boolean, default=False)
    color = Column(String(20), default="#667eea")  # Para visualización

    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    organization = relationship("Organization", back_populates="eventos")
    venta = relationship("Venta", foreign_keys=[venta_id])
    compra = relationship("Compra", foreign_keys=[compra_id])
    producto = relationship("Producto", foreign_keys=[producto_id])
