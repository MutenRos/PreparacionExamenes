"""Models for Oficina Técnica - Bill of Materials (BOM) management."""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from dario_app.database import Base
import enum


class TipoOperacion(str, enum.Enum):
    """Types of manufacturing operations."""
    MECANIZADO_INTERNO = "mecanizado_interno"
    MECANIZADO_EXTERNO = "mecanizado_externo"
    ENSAMBLAJE = "ensamblaje"
    CONTROL_CALIDAD = "control_calidad"
    PINTURA = "pintura"
    SOLDADURA = "soldadura"


class UnidadMedida(str, enum.Enum):
    """Units of measure."""
    UNIDAD = "unidad"
    KG = "kg"
    METRO = "metro"
    LITRO = "litro"


class BOMHeader(Base):
    """Bill of Materials Header - defines the recipe for a product."""
    
    __tablename__ = "bom_headers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Product this BOM is for (the finished product)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False, index=True)
    
    nombre = Column(String(200), nullable=False)  # e.g., "BOM Bomba Centrífuga BC-100"
    codigo = Column(String(50), unique=True, nullable=False, index=True)  # e.g., "BOM-BC100-001"
    version = Column(String(20), default="1.0")
    
    # Quantity this BOM produces
    cantidad_producida = Column(Float, default=1.0)
    unidad_medida = Column(SQLEnum(UnidadMedida), default=UnidadMedida.UNIDAD)
    
    descripcion = Column(Text)
    notas_tecnicas = Column(Text)
    
    activo = Column(Boolean, default=True)
    es_principal = Column(Boolean, default=True)  # Main BOM for this product
    
    # Relationships
    lineas = relationship("BOMLine", back_populates="bom_header", cascade="all, delete-orphan")
    operaciones = relationship("BOMOperacion", back_populates="bom_header", cascade="all, delete-orphan")
    producto = relationship("Producto", foreign_keys=[producto_id])


class BOMLine(Base):
    """Bill of Materials Line - components/materials needed."""
    
    __tablename__ = "bom_lines"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    bom_header_id = Column(Integer, ForeignKey("bom_headers.id"), nullable=False, index=True)
    componente_id = Column(Integer, ForeignKey("productos.id"), nullable=False, index=True)
    
    cantidad = Column(Float, nullable=False)  # Quantity needed
    unidad_medida = Column(SQLEnum(UnidadMedida), default=UnidadMedida.UNIDAD)
    
    secuencia = Column(Integer, default=10)  # Order for display
    es_opcional = Column(Boolean, default=False)
    notas = Column(Text)
    
    # Scrap/waste factor (e.g., 5% for cutting operations)
    factor_desperdicio = Column(Float, default=0.0)  # 0.05 = 5%
    
    # Relationships
    bom_header = relationship("BOMHeader", back_populates="lineas")
    componente = relationship("Producto", foreign_keys=[componente_id])


class BOMOperacion(Base):
    """Manufacturing operations required for the BOM."""
    
    __tablename__ = "bom_operaciones"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    bom_header_id = Column(Integer, ForeignKey("bom_headers.id"), nullable=False, index=True)
    
    nombre = Column(String(200), nullable=False)  # e.g., "Mecanizado eje principal"
    codigo = Column(String(50))
    tipo_operacion = Column(SQLEnum(TipoOperacion), nullable=False)
    
    secuencia = Column(Integer, default=10)
    duracion_estimada = Column(Float)  # Hours
    
    # Centro de trabajo / Workstation
    centro_trabajo = Column(String(100))  # e.g., "Torno CNC 01", "Ensamblaje Linea A"
    
    # Para operaciones externas
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    costo_operacion = Column(Float, default=0.0)
    
    descripcion = Column(Text)
    instrucciones = Column(Text)
    
    # Relationships
    bom_header = relationship("BOMHeader", back_populates="operaciones")
    proveedor = relationship("Proveedor", foreign_keys=[proveedor_id])
