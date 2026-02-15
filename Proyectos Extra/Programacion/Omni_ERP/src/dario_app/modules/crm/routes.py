"""CRM API routes - Leads, Opportunities, Activities, Customer Scores."""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db
from dario_app.modules.usuarios.models import Usuario
from .models import Lead, Opportunity, Activity, CustomerScore
from .service import CRMService


router = APIRouter(prefix="/api/crm", tags=["CRM"])


# ========== LEAD SCHEMAS ==========

class LeadCreate(BaseModel):
    nombre: str
    apellidos: Optional[str] = None
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    website: Optional[str] = None
    source: str = "web"
    source_details: Optional[str] = None
    notas: Optional[str] = None


class LeadUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    website: Optional[str] = None
    status: Optional[str] = None
    assigned_to_id: Optional[int] = None
    notas: Optional[str] = None


class LeadResponse(BaseModel):
    id: int
    nombre: str
    apellidos: Optional[str]
    empresa: Optional[str]
    email: Optional[str]
    telefono: Optional[str]
    source: str
    status: str
    score: int
    valor_estimado: Optional[float]
    assigned_to_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== OPPORTUNITY SCHEMAS ==========

class OpportunityCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    cliente_id: Optional[int] = None
    cliente_nombre: Optional[str] = None
    valor_estimado: float
    probabilidad: int = 50
    stage: str = "prospecting"
    expected_close_date: Optional[datetime] = None
    productos_interes: Optional[List[int]] = None
    competidores: Optional[str] = None


class OpportunityUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    valor_estimado: Optional[float] = None
    probabilidad: Optional[int] = None
    stage: Optional[str] = None
    expected_close_date: Optional[datetime] = None
    loss_reason: Optional[str] = None
    loss_details: Optional[str] = None


class OpportunityResponse(BaseModel):
    id: int
    nombre: str
    cliente_nombre: Optional[str]
    valor_estimado: float
    probabilidad: int
    valor_ponderado: float
    stage: str
    expected_close_date: Optional[datetime]
    stage_changed_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== ACTIVITY SCHEMAS ==========

class ActivityCreate(BaseModel):
    tipo: str  # call, meeting, email, task, note
    asunto: str
    descripcion: Optional[str] = None
    related_to_type: Optional[str] = None  # lead, opportunity, customer
    related_to_id: Optional[int] = None
    related_to_name: Optional[str] = None
    prioridad: str = "medium"
    scheduled_at: Optional[datetime] = None
    duracion_minutos: Optional[int] = None


class ActivityUpdate(BaseModel):
    asunto: Optional[str] = None
    descripcion: Optional[str] = None
    status: Optional[str] = None
    prioridad: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    resultado: Optional[str] = None


class ActivityResponse(BaseModel):
    id: int
    tipo: str
    asunto: str
    related_to_type: Optional[str]
    related_to_name: Optional[str]
    status: str
    prioridad: str
    scheduled_at: Optional[datetime]
    assigned_to_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== LEAD ENDPOINTS ==========

@router.post("/leads", response_model=LeadResponse)
async def create_lead(
    lead_data: LeadCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.leads.create"))
):
    """Create a new lead."""
    lead = Lead(
        organization_id=user.organization_id,
        **lead_data.model_dump()
    )
    
    # Calculate initial score
    lead.score = await CRMService.calculate_lead_score(db, lead, user.organization_id)
    
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    
    return lead


@router.get("/leads", response_model=List[LeadResponse])
async def list_leads(
    status: Optional[str] = None,
    min_score: Optional[int] = None,
    assigned_to_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.leads.read"))
):
    """List all leads with optional filters."""
    query = select(Lead).where(Lead.organization_id == user.organization_id)
    
    if status:
        query = query.where(Lead.status == status)
    if min_score is not None:
        query = query.where(Lead.score >= min_score)
    if assigned_to_id:
        query = query.where(Lead.assigned_to_id == assigned_to_id)
    
    query = query.order_by(Lead.score.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.leads.read"))
):
    """Get a specific lead."""
    stmt = select(Lead).where(
        Lead.id == lead_id,
        Lead.organization_id == user.organization_id
    )
    result = await db.execute(stmt)
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return lead


@router.patch("/leads/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.leads.update"))
):
    """Update a lead."""
    stmt = select(Lead).where(
        Lead.id == lead_id,
        Lead.organization_id == user.organization_id
    )
    result = await db.execute(stmt)
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    for key, value in lead_data.model_dump(exclude_unset=True).items():
        setattr(lead, key, value)
    
    # Recalculate score
    lead.score = await CRMService.calculate_lead_score(db, lead, user.organization_id)
    
    await db.commit()
    await db.refresh(lead)
    
    return lead


@router.post("/leads/{lead_id}/convert")
async def convert_lead(
    lead_id: int,
    create_opportunity: bool = True,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.leads.convert"))
):
    """Convert a lead to a customer and optionally create an opportunity."""
    from dario_app.modules.clientes.models import Cliente
    
    stmt = select(Lead).where(
        Lead.id == lead_id,
        Lead.organization_id == user.organization_id
    )
    result = await db.execute(stmt)
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if lead.status == "converted":
        raise HTTPException(status_code=400, detail="Lead already converted")
    
    # Create customer
    cliente = Cliente(
        organization_id=user.organization_id,
        nombre=lead.nombre,
        apellidos=lead.apellidos,
        nombre_fiscal=lead.empresa or f"{lead.nombre} {lead.apellidos or ''}",
        email=lead.email,
        telefono=lead.telefono,
        tipo_cliente="empresa" if lead.empresa else "particular",
        activo=True
    )
    db.add(cliente)
    await db.flush()
    
    # Update lead
    lead.status = "converted"
    lead.converted_to_customer_id = cliente.id
    lead.converted_at = datetime.utcnow()
    
    # Create opportunity if requested
    opp_id = None
    if create_opportunity and lead.valor_estimado:
        opp = Opportunity(
            organization_id=user.organization_id,
            nombre=f"Opportunity from {lead.nombre}",
            cliente_id=cliente.id,
            cliente_nombre=cliente.nombre_fiscal,
            valor_estimado=lead.valor_estimado,
            probabilidad=50,
            stage="qualification"
        )
        opp.valor_ponderado = await CRMService.calculate_opportunity_weighted_value(opp)
        db.add(opp)
        await db.flush()
        
        lead.converted_to_opportunity_id = opp.id
        opp_id = opp.id
    
    await db.commit()
    
    return {
        "success": True,
        "customer_id": cliente.id,
        "opportunity_id": opp_id
    }


# ========== OPPORTUNITY ENDPOINTS ==========

@router.post("/opportunities", response_model=OpportunityResponse)
async def create_opportunity(
    opp_data: OpportunityCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.opportunities.create"))
):
    """Create a new opportunity."""
    opp = Opportunity(
        organization_id=user.organization_id,
        **opp_data.model_dump()
    )
    opp.valor_ponderado = await CRMService.calculate_opportunity_weighted_value(opp)
    
    db.add(opp)
    await db.commit()
    await db.refresh(opp)
    
    return opp


@router.get("/opportunities", response_model=List[OpportunityResponse])
async def list_opportunities(
    stage: Optional[str] = None,
    cliente_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.opportunities.read"))
):
    """List all opportunities."""
    query = select(Opportunity).where(Opportunity.organization_id == user.organization_id)
    
    if stage:
        query = query.where(Opportunity.stage == stage)
    if cliente_id:
        query = query.where(Opportunity.cliente_id == cliente_id)
    
    query = query.order_by(Opportunity.expected_close_date.asc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/opportunities/{opp_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opp_id: int,
    opp_data: OpportunityUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.opportunities.update"))
):
    """Update an opportunity."""
    stmt = select(Opportunity).where(
        Opportunity.id == opp_id,
        Opportunity.organization_id == user.organization_id
    )
    result = await db.execute(stmt)
    opp = result.scalar_one_or_none()
    
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    old_stage = opp.stage
    
    for key, value in opp_data.model_dump(exclude_unset=True).items():
        setattr(opp, key, value)
    
    # Update stage timestamp if changed
    if opp.stage != old_stage:
        opp.stage_changed_at = datetime.utcnow()
        
        # Update close date for closed stages
        if opp.stage in ["closed_won", "closed_lost"]:
            opp.actual_close_date = datetime.utcnow()
    
    # Recalculate weighted value
    opp.valor_ponderado = await CRMService.calculate_opportunity_weighted_value(opp)
    
    await db.commit()
    await db.refresh(opp)
    
    return opp


@router.get("/pipeline")
async def get_pipeline_metrics(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.opportunities.read"))
):
    """Get sales pipeline metrics."""
    return await CRMService.get_pipeline_metrics(db, user.organization_id)


# ========== ACTIVITY ENDPOINTS ==========

@router.post("/activities", response_model=ActivityResponse)
async def create_activity(
    activity_data: ActivityCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.activities.create"))
):
    """Create a new activity."""
    activity = Activity(
        organization_id=user.organization_id,
        assigned_to_id=user.id,
        assigned_to_name=user.nombre_completo,
        **activity_data.model_dump()
    )
    
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    
    return activity


@router.get("/activities", response_model=List[ActivityResponse])
async def list_activities(
    tipo: Optional[str] = None,
    status: Optional[str] = None,
    related_to_type: Optional[str] = None,
    related_to_id: Optional[int] = None,
    assigned_to_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.activities.read"))
):
    """List activities."""
    query = select(Activity).where(Activity.organization_id == user.organization_id)
    
    if tipo:
        query = query.where(Activity.tipo == tipo)
    if status:
        query = query.where(Activity.status == status)
    if related_to_type:
        query = query.where(Activity.related_to_type == related_to_type)
    if related_to_id:
        query = query.where(Activity.related_to_id == related_to_id)
    if assigned_to_id:
        query = query.where(Activity.assigned_to_id == assigned_to_id)
    
    query = query.order_by(Activity.scheduled_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/activities/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity_data: ActivityUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.activities.update"))
):
    """Update an activity."""
    stmt = select(Activity).where(
        Activity.id == activity_id,
        Activity.organization_id == user.organization_id
    )
    result = await db.execute(stmt)
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    for key, value in activity_data.model_dump(exclude_unset=True).items():
        setattr(activity, key, value)
    
    await db.commit()
    await db.refresh(activity)
    
    return activity


# ========== CUSTOMER SCORE ENDPOINTS ==========

@router.get("/customer-scores")
async def list_customer_scores(
    segment: Optional[str] = None,
    min_score: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.scores.read"))
):
    """List customer scores."""
    query = select(CustomerScore).where(CustomerScore.organization_id == user.organization_id)
    
    if segment:
        query = query.where(CustomerScore.segment == segment)
    if min_score is not None:
        query = query.where(CustomerScore.score >= min_score)
    
    query = query.order_by(CustomerScore.score.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/customer-scores/{cliente_id}/calculate")
async def calculate_customer_score(
    cliente_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.scores.calculate"))
):
    """Calculate/recalculate RFM score for a customer."""
    rfm_data = await CRMService.calculate_customer_rfm_score(
        db, user.organization_id, cliente_id
    )
    
    # Upsert score
    stmt = select(CustomerScore).where(
        CustomerScore.organization_id == user.organization_id,
        CustomerScore.cliente_id == cliente_id
    )
    result = await db.execute(stmt)
    score = result.scalar_one_or_none()
    
    if score:
        for key, value in rfm_data.items():
            setattr(score, key, value)
        score.calculated_at = datetime.utcnow()
    else:
        score = CustomerScore(
            organization_id=user.organization_id,
            cliente_id=cliente_id,
            **rfm_data
        )
        db.add(score)
    
    await db.commit()
    await db.refresh(score)
    
    return score


@router.post("/customer-scores/calculate-all")
async def calculate_all_scores(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("crm.scores.calculate"))
):
    """Recalculate scores for all customers (batch operation)."""
    count = await CRMService.update_all_customer_scores(db, user.organization_id)
    return {"success": True, "customers_updated": count}
