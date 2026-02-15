"""Workflow Automation API routes."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from dario_app.core.auth import get_org_id, require_auth, get_tenant_db
from dario_app.services.workflow_service import (
    WorkflowService,
    WorkflowType,
    WorkflowDefinition,
    WorkflowAutomationInstance,
    workflow_service
)
from dario_app.services.audit_service import AuditService, AuditAction

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


# ==================== REQUEST MODELS ====================

class CreateWorkflowDefinitionRequest(BaseModel):
    """Request to create workflow definition."""
    name: str
    workflow_type: str
    description: Optional[str] = None
    approval_rules: List[Dict[str, Any]]
    sla_hours: int = 24
    reminder_hours: int = 4
    escalation_hours: int = 48
    notification_channels: List[str] = ["email", "in_app"]


class SubmitApprovalRequest(BaseModel):
    """Request to submit document for approval."""
    workflow_type: str
    document_type: str
    document_id: int
    document_number: str
    document_data: Dict[str, Any]


class ApprovalActionRequest(BaseModel):
    """Request to approve/reject a step."""
    comments: Optional[str] = None


# ==================== ENDPOINTS ====================

@router.post("/definitions")
async def create_workflow_definition(
    request: CreateWorkflowDefinitionRequest,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
    user_context: dict = Depends(require_auth)
):
    """Create a new workflow definition (template)."""
    
    try:
        workflow_type = WorkflowType(request.workflow_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid workflow type: {request.workflow_type}")
    
    workflow_def = await WorkflowService.create_workflow_definition(
        db=db,
        org_id=org_id,
        name=request.name,
        workflow_type=workflow_type,
        approval_rules=request.approval_rules,
        sla_hours=request.sla_hours,
        notification_channels=request.notification_channels
    )
    
    # Audit log
    await AuditService.log(
        db=db,
        organization_id=org_id,
        action=AuditAction.CREATE,
        resource_type="workflow_definition",
        resource_id=str(workflow_def.id),
        user_id=user_context["user_id"],
        description=f"Created workflow definition: {request.name}"
    )
    
    return {
        "id": workflow_def.id,
        "name": workflow_def.name,
        "workflow_type": workflow_def.workflow_type,
        "sla_hours": workflow_def.sla_hours,
        "is_active": workflow_def.is_active
    }


@router.get("/definitions")
async def list_workflow_definitions(
    workflow_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """List all workflow definitions."""
    
    from sqlalchemy import select
    
    query = select(WorkflowDefinition).where(
        WorkflowDefinition.organization_id == org_id
    )
    
    if workflow_type:
        query = query.where(WorkflowDefinition.workflow_type == workflow_type)
    
    result = await db.execute(query)
    definitions = result.scalars().all()
    
    return {
        "count": len(definitions),
        "definitions": [
            {
                "id": d.id,
                "name": d.name,
                "workflow_type": d.workflow_type,
                "sla_hours": d.sla_hours,
                "is_active": d.is_active,
                "created_at": d.created_at.isoformat()
            }
            for d in definitions
        ]
    }


@router.post("/submit")
async def submit_for_approval(
    request: SubmitApprovalRequest,
    req: Request,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
    user_context: dict = Depends(require_auth)
):
    """Submit a document for approval."""
    
    try:
        workflow_type = WorkflowType(request.workflow_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid workflow type: {request.workflow_type}")
    
    try:
        instance = await WorkflowService.submit_for_approval(
            db=db,
            org_id=org_id,
            workflow_type=workflow_type,
            document_type=request.document_type,
            document_id=request.document_id,
            document_number=request.document_number,
            requester_id=user_context["user_id"],
            requester_name=user_context.get("name", user_context["email"]),
            requester_email=user_context["email"],
            document_data=request.document_data
        )
        
        # Audit log
        await AuditService.log(
            db=db,
            organization_id=org_id,
            action=AuditAction.CREATE,
            resource_type="workflow_instance",
            resource_id=str(instance.id),
            user_id=user_context["user_id"],
            description=f"Submitted {request.document_type} #{request.document_number} for approval",
            ip_address=req.client.host if req.client else None
        )
        
        return {
            "workflow_id": instance.id,
            "status": instance.status,
            "submitted_at": instance.submitted_at.isoformat(),
            "due_at": instance.due_at.isoformat() if instance.due_at else None,
            "message": "Document submitted for approval successfully"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pending")
async def get_pending_approvals(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
    user_context: dict = Depends(require_auth)
):
    """Get pending approvals for current user."""
    
    approvals = await WorkflowService.get_pending_approvals(
        db=db,
        approver_id=user_context["user_id"],
        org_id=org_id
    )
    
    return {
        "count": len(approvals),
        "approvals": approvals
    }


@router.post("/steps/{step_id}/approve")
async def approve_step(
    step_id: int,
    request: ApprovalActionRequest,
    req: Request,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
    user_context: dict = Depends(require_auth)
):
    """Approve a workflow step."""
    
    try:
        result = await WorkflowService.approve_step(
            db=db,
            step_id=step_id,
            approver_id=user_context["user_id"],
            comments=request.comments,
            ip_address=req.client.host if req.client else None
        )
        
        # Audit log
        await AuditService.log(
            db=db,
            organization_id=org_id,
            action=AuditAction.UPDATE,
            resource_type="workflow_approval",
            resource_id=str(step_id),
            user_id=user_context["user_id"],
            description=f"Approved workflow step #{step_id}",
            ip_address=req.client.host if req.client else None
        )
        
        return {
            "success": True,
            "result": result,
            "message": "Approval recorded successfully"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/steps/{step_id}/reject")
async def reject_step(
    step_id: int,
    request: ApprovalActionRequest,
    req: Request,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
    user_context: dict = Depends(require_auth)
):
    """Reject a workflow step."""
    
    if not request.comments:
        raise HTTPException(status_code=400, detail="Comments are required when rejecting")
    
    try:
        result = await WorkflowService.reject_step(
            db=db,
            step_id=step_id,
            approver_id=user_context["user_id"],
            comments=request.comments,
            ip_address=req.client.host if req.client else None
        )
        
        # Audit log
        await AuditService.log(
            db=db,
            organization_id=org_id,
            action=AuditAction.UPDATE,
            resource_type="workflow_approval",
            resource_id=str(step_id),
            user_id=user_context["user_id"],
            description=f"Rejected workflow step #{step_id}",
            changes={"reason": request.comments},
            ip_address=req.client.host if req.client else None
        )
        
        return {
            "success": True,
            "result": result,
            "message": "Rejection recorded successfully"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/instances/{workflow_id}")
async def get_workflow_instance(
    workflow_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get workflow instance details."""
    
    from sqlalchemy import select
    from dario_app.services.workflow_service import WorkflowApprovalStep
    
    # Get instance
    query = select(WorkflowAutomationInstance).where(
        WorkflowAutomationInstance.id == workflow_id,
        WorkflowAutomationInstance.organization_id == org_id
    )
    result = await db.execute(query)
    instance = result.scalar_one_or_none()
    
    if not instance:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    
    # Get steps
    steps_query = select(WorkflowApprovalStep).where(
        WorkflowApprovalStep.workflow_instance_id == workflow_id
    ).order_by(WorkflowApprovalStep.level, WorkflowApprovalStep.id)
    
    steps_result = await db.execute(steps_query)
    steps = steps_result.scalars().all()
    
    return {
        "id": instance.id,
        "document_type": instance.document_type,
        "document_id": instance.document_id,
        "document_number": instance.document_number,
        "status": instance.status,
        "current_level": instance.current_level,
        "requester_name": instance.requester_name,
        "submitted_at": instance.submitted_at.isoformat(),
        "due_at": instance.due_at.isoformat() if instance.due_at else None,
        "completed_at": instance.completed_at.isoformat() if instance.completed_at else None,
        "escalated": instance.escalated,
        "steps": [
            {
                "id": step.id,
                "level": step.level,
                "approver_name": step.approver_name,
                "status": step.status,
                "action": step.action,
                "assigned_at": step.assigned_at.isoformat(),
                "actioned_at": step.actioned_at.isoformat() if step.actioned_at else None,
                "comments": step.comments
            }
            for step in steps
        ]
    }


@router.get("/instances")
async def list_workflow_instances(
    status: Optional[str] = None,
    document_type: Optional[str] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """List workflow instances."""
    
    from sqlalchemy import select
    
    query = select(WorkflowAutomationInstance).where(
        WorkflowAutomationInstance.organization_id == org_id
    )
    
    if status:
        query = query.where(WorkflowAutomationInstance.status == status)
    
    if document_type:
        query = query.where(WorkflowAutomationInstance.document_type == document_type)
    
    query = query.order_by(WorkflowAutomationInstance.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    instances = result.scalars().all()
    
    return {
        "count": len(instances),
        "instances": [
            {
                "id": inst.id,
                "document_type": inst.document_type,
                "document_number": inst.document_number,
                "status": inst.status,
                "requester_name": inst.requester_name,
                "submitted_at": inst.submitted_at.isoformat(),
                "due_at": inst.due_at.isoformat() if inst.due_at else None
            }
            for inst in instances
        ]
    }


@router.get("/types")
async def list_workflow_types():
    """List available workflow types."""
    return {
        "workflow_types": [
            {
                "value": wf_type.value,
                "name": wf_type.value.replace("_", " ").title()
            }
            for wf_type in WorkflowType
        ]
    }


@router.get("/dashboard")
async def get_workflow_dashboard(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
    user_context: dict = Depends(require_auth)
):
    """Get workflow dashboard metrics."""
    
    from sqlalchemy import select, func
    
    # Pending approvals for user
    pending_count = await db.execute(
        select(func.count()).select_from(
            select(WorkflowApprovalStep).where(
                WorkflowApprovalStep.approver_id == user_context["user_id"],
                WorkflowApprovalStep.status == "pending"
            ).subquery()
        )
    )
    
    # Active workflows in org
    active_query = select(func.count()).select_from(
        select(WorkflowAutomationInstance).where(
            WorkflowAutomationInstance.organization_id == org_id,
            WorkflowAutomationInstance.status.in_(["pending", "in_progress"])
        ).subquery()
    )
    active_count = await db.execute(active_query)
    
    # Overdue workflows
    overdue_query = select(func.count()).select_from(
        select(WorkflowAutomationInstance).where(
            WorkflowAutomationInstance.organization_id == org_id,
            WorkflowAutomationInstance.status.in_(["pending", "in_progress"]),
            WorkflowAutomationInstance.due_at < datetime.utcnow()
        ).subquery()
    )
    overdue_count = await db.execute(overdue_query)
    
    return {
        "my_pending_approvals": pending_count.scalar(),
        "active_workflows": active_count.scalar(),
        "overdue_workflows": overdue_count.scalar()
    }
