"""
Workflow Execution API - Endpoints para ejecutar workflows
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from dario_app.core.dependencies import get_db
from dario_app.core.auth import get_current_user_org
from dario_app.models.workflow_instance import WorkflowInstance, WorkflowTransition
from dario_app.services.workflow_engine import WorkflowEngine


router = APIRouter(prefix="/api/workflows", tags=["workflows"])


# Schemas
class StartWorkflowRequest(BaseModel):
    workflow_name: str
    workflow_graph: Dict[str, Any]
    context_data: Optional[Dict[str, Any]] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None


class TransitionRequest(BaseModel):
    to_node_id: Optional[str] = None
    edge_label: Optional[str] = None


class UpdateContextRequest(BaseModel):
    context_updates: Dict[str, Any]


class WorkflowInstanceResponse(BaseModel):
    id: int
    workflow_name: str
    current_node_id: str
    status: str
    context_data: Dict[str, Any]
    entity_type: Optional[str]
    entity_id: Optional[int]
    created_at: str
    updated_at: str
    completed_at: Optional[str]

    class Config:
        from_attributes = True


@router.post("/execute", response_model=WorkflowInstanceResponse)
async def start_workflow(
    request: StartWorkflowRequest,
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_current_user_org)
):
    """Iniciar una nueva instancia de workflow"""
    engine = WorkflowEngine(db)
    
    instance = await engine.start_workflow(
        organization_id=org_id,
        workflow_name=request.workflow_name,
        workflow_graph=request.workflow_graph,
        context_data=request.context_data,
        entity_type=request.entity_type,
        entity_id=request.entity_id
    )
    
    return WorkflowInstanceResponse(
        id=instance.id,
        workflow_name=instance.workflow_name,
        current_node_id=instance.current_node_id,
        status=instance.status,
        context_data=instance.context_data or {},
        entity_type=instance.entity_type,
        entity_id=instance.entity_id,
        created_at=instance.created_at.isoformat(),
        updated_at=instance.updated_at.isoformat(),
        completed_at=instance.completed_at.isoformat() if instance.completed_at else None
    )


@router.get("/instances", response_model=List[WorkflowInstanceResponse])
async def list_workflow_instances(
    status: Optional[str] = None,
    entity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_current_user_org)
):
    """Listar instancias de workflows"""
    from sqlalchemy import select
    
    query = select(WorkflowInstance).filter(
        WorkflowInstance.organization_id == org_id
    )
    
    if status:
        query = query.filter(WorkflowInstance.status == status)
    
    if entity_type:
        query = query.filter(WorkflowInstance.entity_type == entity_type)
    
    result = await db.execute(
        query.order_by(WorkflowInstance.created_at.desc()).limit(100)
    )
    instances = result.scalars().all()
    
    return [
        WorkflowInstanceResponse(
            id=i.id,
            workflow_name=i.workflow_name,
            current_node_id=i.current_node_id,
            status=i.status,
            context_data=i.context_data or {},
            entity_type=i.entity_type,
            entity_id=i.entity_id,
            created_at=i.created_at.isoformat(),
            updated_at=i.updated_at.isoformat(),
            completed_at=i.completed_at.isoformat() if i.completed_at else None
        )
        for i in instances
    ]


@router.get("/instances/{instance_id}", response_model=WorkflowInstanceResponse)
async def get_workflow_instance(
    instance_id: int,
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_current_user_org)
):
    """Obtener detalles de una instancia"""
    instance = await db.get(WorkflowInstance, instance_id)
    
    if not instance or instance.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    
    return WorkflowInstanceResponse(
        id=instance.id,
        workflow_name=instance.workflow_name,
        current_node_id=instance.current_node_id,
        status=instance.status,
        context_data=instance.context_data or {},
        entity_type=instance.entity_type,
        entity_id=instance.entity_id,
        created_at=instance.created_at.isoformat(),
        updated_at=instance.updated_at.isoformat(),
        completed_at=instance.completed_at.isoformat() if instance.completed_at else None
    )


@router.post("/instances/{instance_id}/transition", response_model=WorkflowInstanceResponse)
async def transition_workflow(
    instance_id: int,
    request: TransitionRequest,
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_current_user_org)
):
    """Hacer una transición en el workflow"""
    instance = await db.get(WorkflowInstance, instance_id)
    
    if not instance or instance.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    
    if instance.status != "running":
        raise HTTPException(status_code=400, detail="Workflow is not running")
    
    engine = WorkflowEngine(db)
    updated_instance = await engine.transition(
        instance,
        to_node_id=request.to_node_id,
        edge_label=request.edge_label
    )
    
    return WorkflowInstanceResponse(
        id=updated_instance.id,
        workflow_name=updated_instance.workflow_name,
        current_node_id=updated_instance.current_node_id,
        status=updated_instance.status,
        context_data=updated_instance.context_data or {},
        entity_type=updated_instance.entity_type,
        entity_id=updated_instance.entity_id,
        created_at=updated_instance.created_at.isoformat(),
        updated_at=updated_instance.updated_at.isoformat(),
        completed_at=updated_instance.completed_at.isoformat() if updated_instance.completed_at else None
    )


@router.patch("/instances/{instance_id}/context", response_model=WorkflowInstanceResponse)
async def update_workflow_context(
    instance_id: int,
    request: UpdateContextRequest,
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_current_user_org)
):
    """Actualizar el contexto de datos de un workflow"""
    instance = await db.get(WorkflowInstance, instance_id)
    
    if not instance or instance.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    
    engine = WorkflowEngine(db)
    updated_instance = await engine.update_context(instance, request.context_updates)
    
    return WorkflowInstanceResponse(
        id=updated_instance.id,
        workflow_name=updated_instance.workflow_name,
        current_node_id=updated_instance.current_node_id,
        status=updated_instance.status,
        context_data=updated_instance.context_data or {},
        entity_type=updated_instance.entity_type,
        entity_id=updated_instance.entity_id,
        created_at=updated_instance.created_at.isoformat(),
        updated_at=updated_instance.updated_at.isoformat(),
        completed_at=updated_instance.completed_at.isoformat() if updated_instance.completed_at else None
    )


@router.get("/instances/{instance_id}/history")
async def get_workflow_history(
    instance_id: int,
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_current_user_org)
):
    """Obtener historial de transiciones de un workflow"""
    instance = await db.get(WorkflowInstance, instance_id)
    
    if not instance or instance.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    
    engine = WorkflowEngine(db)
    history = await engine.get_instance_history(instance_id)
    
    return {"history": history}
