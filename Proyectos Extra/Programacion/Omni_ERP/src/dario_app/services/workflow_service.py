"""Workflow Automation Engine - Microsoft Dynamics 365 style.

This module implements a complete workflow and approval system similar to
Dynamics 365 Business Central and Finance & Operations.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Numeric, Index, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class WorkflowStatus(str, Enum):
    """Workflow instance status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ApprovalAction(str, Enum):
    """Approval actions."""
    APPROVE = "approve"
    REJECT = "reject"
    DELEGATE = "delegate"
    REQUEST_INFO = "request_info"


class WorkflowType(str, Enum):
    """Types of workflows."""
    PURCHASE_ORDER = "purchase_order"
    EXPENSE_REPORT = "expense_report"
    PRICE_CHANGE = "price_change"
    CUSTOMER_CREDIT = "customer_credit"
    VENDOR_APPROVAL = "vendor_approval"
    DISCOUNT_APPROVAL = "discount_approval"
    PAYMENT_APPROVAL = "payment_approval"
    DOCUMENT_APPROVAL = "document_approval"


class NotificationChannel(str, Enum):
    """Notification delivery channels."""
    EMAIL = "email"
    WEBHOOK = "webhook"
    IN_APP = "in_app"
    SMS = "sms"


# ==================== MODELS ====================

class WorkflowDefinition(Base):
    """Workflow definition/template (like Dynamics 365 Workflow Templates)."""
    __tablename__ = "workflow_definitions"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    workflow_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Approval rules (JSON)
    approval_rules: Mapped[str] = mapped_column(JSON, nullable=False)
    # Example: [
    #   {"level": 1, "approver_role": "supervisor", "condition": "amount < 5000"},
    #   {"level": 2, "approver_role": "manager", "condition": "amount >= 5000"},
    #   {"level": 3, "approver_role": "director", "condition": "amount >= 50000"}
    # ]
    
    # SLA settings
    sla_hours: Mapped[int] = mapped_column(Integer, default=24)
    reminder_hours: Mapped[int] = mapped_column(Integer, default=4)
    escalation_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    escalation_hours: Mapped[int] = mapped_column(Integer, default=48)
    
    # Notification settings
    notification_channels: Mapped[str] = mapped_column(JSON, nullable=False, default=["email", "in_app"])
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkflowAutomationInstance(Base):
    """Workflow instance (running workflow for a specific document)."""
    __tablename__ = "workflow_automation_instances"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    workflow_definition_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflow_definitions.id"), nullable=False)
    
    # Document reference
    document_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    document_number: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Workflow state
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    current_level: Mapped[int] = mapped_column(Integer, default=1)
    
    # Requester info
    requester_id: Mapped[int] = mapped_column(Integer, nullable=False)
    requester_name: Mapped[str] = mapped_column(String(200), nullable=False)
    requester_email: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Document data (JSON snapshot)
    document_data: Mapped[str] = mapped_column(JSON, nullable=True)
    
    # Timing
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Escalation
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    escalated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Comments/notes
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkflowApprovalStep(Base):
    """Individual approval step in a workflow."""
    __tablename__ = "workflow_approval_steps"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workflow_instance_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflow_automation_instances.id"), nullable=False, index=True)
    
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    approver_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    approver_name: Mapped[str] = mapped_column(String(200), nullable=False)
    approver_email: Mapped[str] = mapped_column(String(200), nullable=True)
    
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    action: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Timing
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    due_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    actioned_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Approval details
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Delegation
    delegated_to_id: Mapped[int] = mapped_column(Integer, nullable=True)
    delegated_to_name: Mapped[str] = mapped_column(String(200), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkflowNotification(Base):
    """Workflow notifications sent to approvers."""
    __tablename__ = "workflow_notifications"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workflow_instance_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflow_automation_instances.id"), nullable=False, index=True)
    workflow_step_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflow_approval_steps.id"), nullable=True)
    
    recipient_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    recipient_email: Mapped[str] = mapped_column(String(200), nullable=True)
    
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False)  # request, reminder, escalation, completed
    channel: Mapped[str] = mapped_column(String(20), nullable=False)  # email, webhook, in_app
    
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=True)
    
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Delivery status
    delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_error: Mapped[str] = mapped_column(Text, nullable=True)


class JobQueue(Base):
    """Job queue for async batch processing (like Dynamics 365 Job Queue)."""
    __tablename__ = "job_queue"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    
    job_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    job_name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Job payload (JSON)
    payload: Mapped[str] = mapped_column(JSON, nullable=True)
    
    # Scheduling
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    # pending, running, completed, failed, cancelled
    
    priority: Mapped[int] = mapped_column(Integer, default=5)  # 1=highest, 10=lowest
    
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Retry settings
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Results
    result: Mapped[str] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== SERVICE ====================

class WorkflowService:
    """Workflow automation service - Dynamics 365 style."""
    
    @staticmethod
    async def create_workflow_definition(
        db: AsyncSession,
        org_id: int,
        name: str,
        workflow_type: WorkflowType,
        approval_rules: List[Dict[str, Any]],
        sla_hours: int = 24,
        notification_channels: List[str] = None
    ) -> WorkflowDefinition:
        """Create a new workflow definition."""
        
        if notification_channels is None:
            notification_channels = ["email", "in_app"]
        
        workflow_def = WorkflowDefinition(
            organization_id=org_id,
            name=name,
            workflow_type=workflow_type.value,
            approval_rules=approval_rules,
            sla_hours=sla_hours,
            notification_channels=notification_channels
        )
        
        db.add(workflow_def)
        await db.commit()
        await db.refresh(workflow_def)
        
        return workflow_def
    
    @staticmethod
    async def submit_for_approval(
        db: AsyncSession,
        org_id: int,
        workflow_type: WorkflowType,
        document_type: str,
        document_id: int,
        document_number: str,
        requester_id: int,
        requester_name: str,
        document_data: Dict[str, Any],
        requester_email: Optional[str] = None
    ) -> WorkflowAutomationInstance:
        """Submit a document for approval."""
        
        # Find active workflow definition
        query = select(WorkflowDefinition).where(
            WorkflowDefinition.organization_id == org_id,
            WorkflowDefinition.workflow_type == workflow_type.value,
            WorkflowDefinition.is_active == True
        )
        result = await db.execute(query)
        workflow_def = result.scalar_one_or_none()
        
        if not workflow_def:
            raise ValueError(f"No active workflow definition found for {workflow_type.value}")
        
        # Create workflow instance
        due_at = datetime.utcnow() + timedelta(hours=workflow_def.sla_hours)
        
        instance = WorkflowAutomationInstance(
            organization_id=org_id,
            workflow_definition_id=workflow_def.id,
            document_type=document_type,
            document_id=document_id,
            document_number=document_number,
            requester_id=requester_id,
            requester_name=requester_name,
            requester_email=requester_email,
            document_data=document_data,
            status=WorkflowStatus.PENDING.value,
            current_level=1,
            due_at=due_at
        )
        
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        
        # Create approval steps based on rules
        await WorkflowService._create_approval_steps(db, instance, workflow_def)
        
        # Send notifications to first level approvers
        await WorkflowService._send_approval_notifications(db, instance, workflow_def)
        
        return instance
    
    @staticmethod
    async def _create_approval_steps(
        db: AsyncSession,
        instance: WorkflowAutomationInstance,
        workflow_def: WorkflowDefinition
    ):
        """Create approval steps based on workflow rules."""
        
        approval_rules = workflow_def.approval_rules
        document_data = instance.document_data or {}
        
        for rule in approval_rules:
            level = rule.get("level", 1)
            approver_role = rule.get("approver_role")
            condition = rule.get("condition", "true")
            
            # Evaluate condition (simplified - in production use a proper expression evaluator)
            should_create = True
            if "amount" in condition and "amount" in document_data:
                amount = float(document_data.get("amount", 0))
                if "<" in condition:
                    threshold = float(condition.split("<")[1].strip())
                    should_create = amount < threshold
                elif ">=" in condition:
                    threshold = float(condition.split(">=")[1].strip())
                    should_create = amount >= threshold
            
            if should_create:
                # Find approver by role (simplified - in production query users table)
                approver_id = rule.get("approver_id", 1)  # Default to admin
                approver_name = rule.get("approver_name", "Approver")
                approver_email = rule.get("approver_email")
                
                step = WorkflowApprovalStep(
                    workflow_instance_id=instance.id,
                    level=level,
                    approver_id=approver_id,
                    approver_name=approver_name,
                    approver_email=approver_email,
                    status=WorkflowStatus.PENDING.value,
                    due_at=instance.due_at
                )
                
                db.add(step)
        
        await db.commit()
    
    @staticmethod
    async def _send_approval_notifications(
        db: AsyncSession,
        instance: WorkflowAutomationInstance,
        workflow_def: WorkflowDefinition
    ):
        """Send notifications to approvers."""
        
        # Get pending steps for current level
        query = select(WorkflowApprovalStep).where(
            WorkflowApprovalStep.workflow_instance_id == instance.id,
            WorkflowApprovalStep.level == instance.current_level,
            WorkflowApprovalStep.status == WorkflowStatus.PENDING.value
        )
        result = await db.execute(query)
        steps = result.scalars().all()
        
        for step in steps:
            for channel in workflow_def.notification_channels:
                notification = WorkflowNotification(
                    workflow_instance_id=instance.id,
                    workflow_step_id=step.id,
                    recipient_id=step.approver_id,
                    recipient_email=step.approver_email,
                    notification_type="request",
                    channel=channel,
                    subject=f"Approval Required: {instance.document_type} #{instance.document_number}",
                    body=f"You have a pending approval request from {instance.requester_name}.",
                    delivered=False
                )
                db.add(notification)
        
        await db.commit()
    
    @staticmethod
    async def approve_step(
        db: AsyncSession,
        step_id: int,
        approver_id: int,
        comments: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """Approve a workflow step."""
        
        # Get step
        query = select(WorkflowApprovalStep).where(WorkflowApprovalStep.id == step_id)
        result = await db.execute(query)
        step = result.scalar_one_or_none()
        
        if not step:
            raise ValueError("Approval step not found")
        
        if step.approver_id != approver_id:
            raise ValueError("Not authorized to approve this step")
        
        if step.status != WorkflowStatus.PENDING.value:
            raise ValueError("Step already processed")
        
        # Update step
        step.status = WorkflowStatus.APPROVED.value
        step.action = ApprovalAction.APPROVE.value
        step.actioned_at = datetime.utcnow()
        step.comments = comments
        step.ip_address = ip_address
        
        # Get workflow instance
        instance_query = select(WorkflowAutomationInstance).where(WorkflowAutomationInstance.id == step.workflow_instance_id)
        instance_result = await db.execute(instance_query)
        instance = instance_result.scalar_one()
        
        # Check if all steps at current level are approved
        level_steps_query = select(WorkflowApprovalStep).where(
            WorkflowApprovalStep.workflow_instance_id == instance.id,
            WorkflowApprovalStep.level == instance.current_level
        )
        level_steps_result = await db.execute(level_steps_query)
        level_steps = level_steps_result.scalars().all()
        
        all_approved = all(s.status == WorkflowStatus.APPROVED.value for s in level_steps)
        
        if all_approved:
            # Check if there are more levels
            next_level_query = select(WorkflowApprovalStep).where(
                WorkflowApprovalStep.workflow_instance_id == instance.id,
                WorkflowApprovalStep.level > instance.current_level
            )
            next_level_result = await db.execute(next_level_query)
            has_next_level = next_level_result.first() is not None
            
            if has_next_level:
                # Move to next level
                instance.current_level += 1
                instance.status = WorkflowStatus.IN_PROGRESS.value
                
                # Send notifications for next level
                workflow_def_query = select(WorkflowDefinition).where(
                    WorkflowDefinition.id == instance.workflow_definition_id
                )
                workflow_def_result = await db.execute(workflow_def_query)
                workflow_def = workflow_def_result.scalar_one()
                
                await WorkflowService._send_approval_notifications(db, instance, workflow_def)
            else:
                # Workflow complete
                instance.status = WorkflowStatus.APPROVED.value
                instance.completed_at = datetime.utcnow()
        
        await db.commit()
        
        return {
            "step_id": step.id,
            "status": step.status,
            "workflow_status": instance.status,
            "completed": instance.status == WorkflowStatus.APPROVED.value
        }
    
    @staticmethod
    async def reject_step(
        db: AsyncSession,
        step_id: int,
        approver_id: int,
        comments: str,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """Reject a workflow step."""
        
        query = select(WorkflowApprovalStep).where(WorkflowApprovalStep.id == step_id)
        result = await db.execute(query)
        step = result.scalar_one_or_none()
        
        if not step:
            raise ValueError("Approval step not found")
        
        if step.approver_id != approver_id:
            raise ValueError("Not authorized to reject this step")
        
        step.status = WorkflowStatus.REJECTED.value
        step.action = ApprovalAction.REJECT.value
        step.actioned_at = datetime.utcnow()
        step.comments = comments
        step.ip_address = ip_address
        
        # Reject entire workflow
        instance_query = select(WorkflowAutomationInstance).where(WorkflowAutomationInstance.id == step.workflow_instance_id)
        instance_result = await db.execute(instance_query)
        instance = instance_result.scalar_one()
        
        instance.status = WorkflowStatus.REJECTED.value
        instance.completed_at = datetime.utcnow()
        
        await db.commit()
        
        return {
            "step_id": step.id,
            "status": step.status,
            "workflow_status": instance.status
        }
    
    @staticmethod
    async def get_pending_approvals(
        db: AsyncSession,
        approver_id: int,
        org_id: int
    ) -> List[Dict[str, Any]]:
        """Get pending approvals for a user."""
        
        query = select(WorkflowApprovalStep, WorkflowAutomationInstance).join(
            WorkflowAutomationInstance,
            WorkflowAutomationInstance.id == WorkflowApprovalStep.workflow_instance_id
        ).where(
            WorkflowApprovalStep.approver_id == approver_id,
            WorkflowApprovalStep.status == WorkflowStatus.PENDING.value,
            WorkflowAutomationInstance.organization_id == org_id
        ).order_by(WorkflowApprovalStep.due_at)
        
        result = await db.execute(query)
        rows = result.all()
        
        approvals = []
        for step, instance in rows:
            approvals.append({
                "step_id": step.id,
                "workflow_id": instance.id,
                "document_type": instance.document_type,
                "document_id": instance.document_id,
                "document_number": instance.document_number,
                "requester_name": instance.requester_name,
                "submitted_at": instance.submitted_at.isoformat(),
                "due_at": step.due_at.isoformat() if step.due_at else None,
                "level": step.level,
                "document_data": instance.document_data
            })
        
        return approvals
    
    @staticmethod
    async def process_sla_reminders(db: AsyncSession):
        """Process SLA reminders and escalations (run as scheduled job)."""
        
        now = datetime.utcnow()
        
        # Find workflows approaching SLA
        query = select(WorkflowAutomationInstance, WorkflowDefinition).join(
            WorkflowDefinition,
            WorkflowDefinition.id == WorkflowAutomationInstance.workflow_definition_id
        ).where(
            WorkflowAutomationInstance.status.in_([WorkflowStatus.PENDING.value, WorkflowStatus.IN_PROGRESS.value]),
            WorkflowAutomationInstance.due_at.isnot(None)
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        reminders_sent = 0
        escalations_sent = 0
        
        for instance, workflow_def in rows:
            time_until_due = (instance.due_at - now).total_seconds() / 3600  # hours
            time_overdue = (now - instance.due_at).total_seconds() / 3600  # hours
            
            # Send reminder if approaching SLA
            if 0 < time_until_due < workflow_def.reminder_hours:
                # TODO: Send reminder notification
                reminders_sent += 1
            
            # Escalate if overdue
            if time_overdue > 0 and workflow_def.escalation_enabled and not instance.escalated:
                if time_overdue >= workflow_def.escalation_hours:
                    instance.escalated = True
                    instance.escalated_at = now
                    # TODO: Send escalation notification
                    escalations_sent += 1
        
        await db.commit()
        
        return {
            "reminders_sent": reminders_sent,
            "escalations_sent": escalations_sent,
            "processed_at": now.isoformat()
        }


# Global service instance
workflow_service = WorkflowService()
