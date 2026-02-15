"""
Workflow Instance Model - Instancias de workflows en ejecución
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class WorkflowInstance(Base):
    """Instancia de un workflow en ejecución"""
    __tablename__ = "workflow_instances"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Workflow configuration
    workflow_name = Column(String(200), nullable=False)
    workflow_graph = Column(JSON, nullable=False)  # Copia del grafo al momento de iniciar
    
    # Estado actual
    current_node_id = Column(String(50), nullable=False)  # ID del nodo actual (ej: "n1")
    status = Column(String(50), default="running")  # running, completed, failed, paused
    
    # Contexto de datos
    context_data = Column(JSON, default=dict)  # Datos del contexto (stock, total, cliente, etc.)
    
    # Referencias a entidades relacionadas
    entity_type = Column(String(50), nullable=True)  # orden_produccion, orden_compra, venta, etc.
    entity_id = Column(Integer, nullable=True)  # ID de la entidad relacionada
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Historial de transiciones
    transitions = relationship("WorkflowTransition", back_populates="instance", cascade="all, delete-orphan")


class WorkflowTransition(Base):
    """Registro de transiciones entre nodos"""
    __tablename__ = "workflow_transitions"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("workflow_instances.id"), nullable=False)
    
    # Transición
    from_node_id = Column(String(50), nullable=False)
    to_node_id = Column(String(50), nullable=False)
    edge_label = Column(String(100), nullable=True)  # true/false/timeout
    
    # Evaluación de condición (si aplica)
    condition_evaluated = Column(JSON, nullable=True)  # {variable, operator, value, result}
    
    # Acción ejecutada (si aplica)
    action_executed = Column(JSON, nullable=True)  # {action_type, params, result}
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    instance = relationship("WorkflowInstance", back_populates="transitions")


class WorkflowActionLog(Base):
    """Log de acciones ejecutadas por workflows"""
    __tablename__ = "workflow_action_logs"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("workflow_instances.id"), nullable=False)
    
    # Acción
    action_type = Column(String(100), nullable=False)  # send_notification, generate_document, etc.
    action_params = Column(JSON, default=dict)
    
    # Resultado
    status = Column(String(50), nullable=False)  # success, failed
    result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
