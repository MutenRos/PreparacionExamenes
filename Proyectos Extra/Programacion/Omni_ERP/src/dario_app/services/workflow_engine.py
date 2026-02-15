"""
Workflow Execution Engine - Motor de ejecución de workflows
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import operator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dario_app.models.workflow_instance import WorkflowInstance, WorkflowTransition, WorkflowActionLog


class WorkflowEngine:
    """Motor de ejecución de workflows"""
    
    # Operadores de comparación
    OPERATORS = {
        "==": operator.eq,
        "!=": operator.ne,
        "<": operator.lt,
        ">": operator.gt,
        "<=": operator.le,
        ">=": operator.ge,
    }
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def start_workflow(
        self,
        organization_id: int,
        workflow_name: str,
        workflow_graph: Dict[str, Any],
        context_data: Dict[str, Any] = None,
        entity_type: str = None,
        entity_id: int = None
    ) -> WorkflowInstance:
        """
        Iniciar una nueva instancia de workflow
        
        Args:
            organization_id: ID de la organización
            workflow_name: Nombre del workflow
            workflow_graph: Grafo del workflow (nodos y edges)
            context_data: Datos de contexto inicial
            entity_type: Tipo de entidad relacionada
            entity_id: ID de la entidad relacionada
        
        Returns:
            WorkflowInstance creada
        """
        # Encontrar el nodo inicial (primer nodo sin incoming edges)
        nodes = workflow_graph.get("nodes", [])
        edges = workflow_graph.get("edges", [])
        
        # Buscar nodo sin incoming edges
        nodes_with_incoming = set(e["toId"] for e in edges)
        start_nodes = [n for n in nodes if n["id"] not in nodes_with_incoming]
        
        if not start_nodes:
            # Si no hay nodo sin incoming, usar el primero
            start_node_id = nodes[0]["id"] if nodes else "n1"
        else:
            start_node_id = start_nodes[0]["id"]
        
        # Crear instancia
        instance = WorkflowInstance(
            organization_id=organization_id,
            workflow_name=workflow_name,
            workflow_graph=workflow_graph,
            current_node_id=start_node_id,
            status="running",
            context_data=context_data or {},
            entity_type=entity_type,
            entity_id=entity_id
        )
        
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        
        # Ejecutar acciones del nodo inicial si es tipo action
        await self._execute_node_actions(instance, start_node_id)
        
        return instance
    
    def evaluate_condition(
        self,
        condition_props: Dict[str, Any],
        context_data: Dict[str, Any]
    ) -> bool:
        """
        Evaluar una condición contra el contexto
        
        Args:
            condition_props: {variable, operator, value}
            context_data: Datos de contexto
        
        Returns:
            True si la condición se cumple, False si no
        """
        variable = condition_props.get("variable")
        operator_str = condition_props.get("operator", "==")
        value_str = condition_props.get("value")
        
        if not variable or variable not in context_data:
            return False
        
        # Obtener valor del contexto
        context_value = context_data[variable]
        
        # Intentar convertir a número si es posible
        try:
            context_value = float(context_value)
            compare_value = float(value_str)
        except (ValueError, TypeError):
            # Mantener como string si no se puede convertir
            compare_value = value_str
        
        # Aplicar operador
        op_func = self.OPERATORS.get(operator_str, operator.eq)
        return op_func(context_value, compare_value)
    
    async def transition(
        self,
        instance: WorkflowInstance,
        to_node_id: str = None,
        edge_label: str = None
    ) -> WorkflowInstance:
        """
        Hacer una transición a otro nodo
        
        Args:
            instance: Instancia del workflow
            to_node_id: ID del nodo destino (si es None, se calcula automáticamente)
            edge_label: Etiqueta del edge usado (si aplica)
        
        Returns:
            WorkflowInstance actualizada
        """
        current_node_id = instance.current_node_id
        workflow_graph = instance.workflow_graph
        
        # Si no se especifica to_node_id, buscar el siguiente automáticamente
        if to_node_id is None:
            to_node_id = self._find_next_node(instance, current_node_id)
        
        if to_node_id is None:
            # No hay siguiente nodo, marcar como completado
            instance.status = "completed"
            instance.completed_at = datetime.utcnow()
            await self.db.commit()
            return instance
        
        # Registrar transición
        transition = WorkflowTransition(
            instance_id=instance.id,
            from_node_id=current_node_id,
            to_node_id=to_node_id,
            edge_label=edge_label
        )
        self.db.add(transition)
        
        # Actualizar nodo actual
        instance.current_node_id = to_node_id
        instance.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(instance)
        
        # Ejecutar acciones del nuevo nodo
        await self._execute_node_actions(instance, to_node_id)
        
        return instance
    
    def _find_next_node(
        self,
        instance: WorkflowInstance,
        current_node_id: str
    ) -> Optional[str]:
        """Encontrar el siguiente nodo basado en el nodo actual y las condiciones"""
        workflow_graph = instance.workflow_graph
        nodes = {n["id"]: n for n in workflow_graph.get("nodes", [])}
        edges = workflow_graph.get("edges", [])
        
        current_node = nodes.get(current_node_id)
        if not current_node:
            return None
        
        # Buscar edges salientes
        outgoing_edges = [e for e in edges if e["fromId"] == current_node_id]
        
        if not outgoing_edges:
            return None
        
        # Si el nodo actual es condition, evaluar
        if current_node.get("type") == "condition":
            condition_props = current_node.get("props", {})
            result = self.evaluate_condition(condition_props, instance.context_data)
            
            # Buscar edge con label correcto
            target_label = "true" if result else "false"
            for edge in outgoing_edges:
                if edge.get("label") == target_label:
                    return edge["toId"]
            
            # Si no hay edge con label, usar el primero
            return outgoing_edges[0]["toId"] if outgoing_edges else None
        
        # Para otros tipos de nodos, usar el primer edge
        return outgoing_edges[0]["toId"]
    
    async def _execute_node_actions(self, instance: WorkflowInstance, node_id: str):
        """Ejecutar acciones de un nodo (si es tipo action)"""
        workflow_graph = instance.workflow_graph
        nodes = {n["id"]: n for n in workflow_graph.get("nodes", [])}
        
        node = nodes.get(node_id)
        if not node or node.get("type") != "action":
            return
        
        # Determinar tipo de acción basado en el label
        label = node.get("label", "").lower()
        
        action_type = "unknown"
        if "notificación" in label or "notificar" in label:
            action_type = "send_notification"
        elif "documento" in label or "generar" in label:
            action_type = "generate_document"
        elif "asignar usuario" in label:
            action_type = "assign_user"
        elif "asignar sección" in label or "sección" in label:
            action_type = "assign_section"
        
        # Registrar acción
        action_log = WorkflowActionLog(
            instance_id=instance.id,
            action_type=action_type,
            action_params=node.get("props", {}),
            status="success",
            result={"executed": True, "node_id": node_id}
        )
        self.db.add(action_log)
        await self.db.commit()
    
    async def update_context(
        self,
        instance: WorkflowInstance,
        context_updates: Dict[str, Any]
    ) -> WorkflowInstance:
        """Actualizar el contexto de datos de una instancia"""
        current_context = instance.context_data or {}
        current_context.update(context_updates)
        instance.context_data = current_context
        instance.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(instance)
        
        return instance
    
    async def get_instance_history(self, instance_id: int) -> List[Dict[str, Any]]:
        """Obtener historial de transiciones de una instancia"""
        result = await self.db.execute(
            select(WorkflowTransition)
            .filter(WorkflowTransition.instance_id == instance_id)
            .order_by(WorkflowTransition.created_at)
        )
        transitions = result.scalars().all()
        
        return [
            {
                "id": t.id,
                "from_node_id": t.from_node_id,
                "to_node_id": t.to_node_id,
                "edge_label": t.edge_label,
                "condition_evaluated": t.condition_evaluated,
                "action_executed": t.action_executed,
                "created_at": t.created_at.isoformat()
            }
            for t in transitions
        ]
