"""Marketing routes - Campaigns, Email Marketing, Lead Scoring."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import Campaign, CampaignActivity, MarketingList, EmailTemplate, CustomerJourney, LeadScore

router = APIRouter(prefix="/api/marketing", tags=["Marketing"])


# Schemas

class CampaignCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    campaign_type: str = "email"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: float = 0
    target_audience: Optional[str] = None


class CampaignActivityCreate(BaseModel):
    activity_type: str
    subject: str
    descripcion: Optional[str] = None
    scheduled_at: Optional[str] = None
    target_list_id: Optional[int] = None
    email_template_id: Optional[int] = None


class MarketingListCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    list_type: str = "static"
    criteria: Optional[str] = None


class EmailTemplateCreate(BaseModel):
    name: str
    template_type: str = "newsletter"
    subject: str
    html_content: str
    plain_text_content: Optional[str] = None


class CustomerJourneyCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    workflow_definition: Optional[str] = None
    entry_list_id: Optional[int] = None
    entry_trigger: Optional[str] = None


# Campaigns

@router.post("/campaigns")
async def create_campaign(
    payload: CampaignCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.campaigns.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate campaign code
    stmt = select(Campaign).where(Campaign.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    campaign_code = f"CAMP-{datetime.now().strftime('%Y%m')}-{count + 1:04d}"
    
    campaign = Campaign(
        organization_id=org_id,
        campaign_code=campaign_code,
        owner_user_id=user.id,
        owner_name=user.nombre_completo,
        **payload.model_dump()
    )
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


@router.get("/campaigns")
async def list_campaigns(
    status: Optional[str] = None,
    campaign_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.campaigns.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Campaign).where(Campaign.organization_id == org_id)
    if status:
        query = query.where(Campaign.status == status)
    if campaign_type:
        query = query.where(Campaign.campaign_type == campaign_type)
    query = query.order_by(Campaign.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/campaigns/{campaign_id}")
async def get_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.campaigns.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Campaign).where(Campaign.id == campaign_id, Campaign.organization_id == org_id)
    result = await db.execute(stmt)
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/campaigns/{campaign_id}/activate")
async def activate_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.campaigns.activate")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Campaign).where(Campaign.id == campaign_id, Campaign.organization_id == org_id)
    result = await db.execute(stmt)
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign.status = "active"
    await db.commit()
    await db.refresh(campaign)
    return campaign


# Campaign Activities

@router.post("/campaigns/{campaign_id}/activities")
async def create_activity(
    campaign_id: int,
    payload: CampaignActivityCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.campaigns.manage")),
    org_id: int = Depends(get_org_id),
):
    activity = CampaignActivity(
        organization_id=org_id,
        campaign_id=campaign_id,
        **payload.model_dump()
    )
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity


@router.get("/campaigns/{campaign_id}/activities")
async def list_activities(
    campaign_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.campaigns.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CampaignActivity).where(
        CampaignActivity.organization_id == org_id,
        CampaignActivity.campaign_id == campaign_id
    ).order_by(CampaignActivity.created_at)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/campaigns/{campaign_id}/activities/{activity_id}/execute")
async def execute_activity(
    campaign_id: int,
    activity_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.campaigns.execute")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(CampaignActivity).where(
        CampaignActivity.id == activity_id,
        CampaignActivity.campaign_id == campaign_id,
        CampaignActivity.organization_id == org_id
    )
    result = await db.execute(stmt)
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity.status = "executing"
    activity.executed_at = datetime.utcnow()
    await db.commit()
    
    # TODO: Actual email sending logic here
    
    activity.status = "completed"
    await db.commit()
    await db.refresh(activity)
    return activity


# Marketing Lists

@router.post("/lists")
async def create_list(
    payload: MarketingListCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.lists.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate list code
    stmt = select(MarketingList).where(MarketingList.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    list_code = f"LIST-{count + 1:04d}"
    
    mkt_list = MarketingList(
        organization_id=org_id,
        list_code=list_code,
        **payload.model_dump()
    )
    db.add(mkt_list)
    await db.commit()
    await db.refresh(mkt_list)
    return mkt_list


@router.get("/lists")
async def list_marketing_lists(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.lists.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(MarketingList).where(MarketingList.organization_id == org_id)
    if status:
        query = query.where(MarketingList.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Email Templates

@router.post("/email-templates")
async def create_template(
    payload: EmailTemplateCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.templates.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate template code
    stmt = select(EmailTemplate).where(EmailTemplate.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    template_code = f"TMPL-{count + 1:04d}"
    
    template = EmailTemplate(
        organization_id=org_id,
        template_code=template_code,
        **payload.model_dump()
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.get("/email-templates")
async def list_templates(
    template_type: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.templates.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(EmailTemplate).where(EmailTemplate.organization_id == org_id)
    if template_type:
        query = query.where(EmailTemplate.template_type == template_type)
    if status:
        query = query.where(EmailTemplate.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/email-templates/{template_id}")
async def get_template(
    template_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.templates.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(EmailTemplate).where(
        EmailTemplate.id == template_id,
        EmailTemplate.organization_id == org_id
    )
    result = await db.execute(stmt)
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


# Customer Journeys

@router.post("/customer-journeys")
async def create_journey(
    payload: CustomerJourneyCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.journeys.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate journey code
    stmt = select(CustomerJourney).where(CustomerJourney.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    journey_code = f"JOUR-{count + 1:04d}"
    
    journey = CustomerJourney(
        organization_id=org_id,
        journey_code=journey_code,
        **payload.model_dump()
    )
    db.add(journey)
    await db.commit()
    await db.refresh(journey)
    return journey


@router.get("/customer-journeys")
async def list_journeys(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.journeys.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerJourney).where(CustomerJourney.organization_id == org_id)
    if status:
        query = query.where(CustomerJourney.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/customer-journeys/{journey_id}/activate")
async def activate_journey(
    journey_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.journeys.activate")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(CustomerJourney).where(
        CustomerJourney.id == journey_id,
        CustomerJourney.organization_id == org_id
    )
    result = await db.execute(stmt)
    journey = result.scalar_one_or_none()
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")
    
    journey.status = "active"
    await db.commit()
    await db.refresh(journey)
    return journey


# Lead Scoring

@router.post("/lead-scores")
async def create_lead_score(
    lead_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.scoring.manage")),
    org_id: int = Depends(get_org_id),
):
    # Check if score already exists
    stmt = select(LeadScore).where(
        LeadScore.organization_id == org_id,
        LeadScore.lead_id == lead_id
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    
    score = LeadScore(
        organization_id=org_id,
        lead_id=lead_id,
        total_score=0
    )
    db.add(score)
    await db.commit()
    await db.refresh(score)
    return score


@router.get("/lead-scores")
async def list_lead_scores(
    min_score: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.scoring.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(LeadScore).where(LeadScore.organization_id == org_id)
    if min_score:
        query = query.where(LeadScore.total_score >= min_score)
    query = query.order_by(LeadScore.total_score.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/lead-scores/{lead_id}/update")
async def update_lead_score(
    lead_id: int,
    demographic_score: int = 0,
    behavioral_score: int = 0,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("marketing.scoring.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(LeadScore).where(
        LeadScore.organization_id == org_id,
        LeadScore.lead_id == lead_id
    )
    result = await db.execute(stmt)
    score = result.scalar_one_or_none()
    if not score:
        raise HTTPException(status_code=404, detail="Lead score not found")
    
    score.demographic_score = demographic_score
    score.behavioral_score = behavioral_score
    score.total_score = demographic_score + behavioral_score
    
    # Assign grade
    if score.total_score >= 90:
        score.grade = "A"
    elif score.total_score >= 75:
        score.grade = "B"
    elif score.total_score >= 60:
        score.grade = "C"
    elif score.total_score >= 40:
        score.grade = "D"
    else:
        score.grade = "F"
    
    score.last_activity_at = datetime.utcnow()
    await db.commit()
    await db.refresh(score)
    return score
