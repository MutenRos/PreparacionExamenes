"""Advanced Marketing API routes (Dynamics 365 parity)."""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
import uuid

from dario_app.database import get_db

router = APIRouter(prefix="/marketing_advanced", tags=["Marketing"])


# ============ Pydantic Models ============

class CampaignCreate(BaseModel):
    name: str
    campaign_type: str
    start_date: datetime
    end_date: datetime
    budget: float = 0.0
    status: str = "Draft"


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    actual_cost: Optional[float] = None
    total_leads: Optional[int] = None


class ActivityCreate(BaseModel):
    campaign_id: str
    name: str
    activity_type: str
    channel: str
    scheduled_date: datetime


class ListCreate(BaseModel):
    name: str
    list_type: str
    description: Optional[str] = None


class TemplateCreate(BaseModel):
    name: str
    category: str
    subject_line: str
    html_content: str


class JourneyCreate(BaseModel):
    name: str
    journey_type: str
    description: Optional[str] = None


class LeadScoringCreate(BaseModel):
    name: str
    model_type: str
    scoring_rules: list = []


# ============ Campaign Endpoints ============

@router.post("/campaigns")
async def create_campaign(data: CampaignCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create marketing campaign."""
    from dario_app.modules.marketing_advanced.models import MarketingCampaign
    
    campaign = MarketingCampaign(
        organization_id=org_id,
        campaign_code=f"CAM-{datetime.now().strftime('%Y')}-{str(uuid.uuid4())[:5].upper()}",
        name=data.name,
        campaign_type=data.campaign_type,
        start_date=data.start_date,
        end_date=data.end_date,
        budget=data.budget,
        status=data.status
    )
    session.add(campaign)
    await session.commit()
    return {"campaign_id": campaign.id, "campaign_code": campaign.campaign_code, "status": "created"}


@router.get("/campaigns")
async def list_campaigns(session: AsyncSession = Depends(get_db), status: Optional[str] = None, org_id: str = "default"):
    """List marketing campaigns with optional filtering."""
    from dario_app.modules.marketing_advanced.models import MarketingCampaign
    
    query = select(MarketingCampaign).where(MarketingCampaign.organization_id == org_id)
    if status:
        query = query.where(MarketingCampaign.status == status)
    
    result = await session.execute(query)
    campaigns = result.scalars().all()
    return {
        "total": len(campaigns),
        "campaigns": [
            {
                "id": c.id,
                "campaign_code": c.campaign_code,
                "name": c.name,
                "status": c.status,
                "budget": c.budget,
                "actual_cost": c.actual_cost,
                "total_leads": c.total_leads,
                "roi_percent": c.roi_percent
            }
            for c in campaigns
        ]
    }


@router.patch("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: str, data: CampaignUpdate, session: AsyncSession = Depends(get_db)):
    """Update campaign details."""
    from dario_app.modules.marketing_advanced.models import MarketingCampaign
    
    campaign = await session.get(MarketingCampaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(campaign, field, value)
    
    await session.commit()
    return {"message": "Campaign updated", "campaign_id": campaign_id}


# ============ Activity Endpoints ============

@router.post("/activities")
async def create_activity(data: ActivityCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create marketing activity."""
    from dario_app.modules.marketing_advanced.models import MarketingActivity
    
    activity = MarketingActivity(
        organization_id=org_id,
        activity_code=f"ACT-{uuid.uuid4().hex[:8].upper()}",
        campaign_id=data.campaign_id,
        name=data.name,
        activity_type=data.activity_type,
        channel=data.channel,
        scheduled_date=data.scheduled_date,
        status="Planned"
    )
    session.add(activity)
    await session.commit()
    return {"activity_id": activity.id, "activity_code": activity.activity_code}


@router.get("/campaigns/{campaign_id}/activities")
async def get_campaign_activities(campaign_id: str, session: AsyncSession = Depends(get_db)):
    """Get all activities for a campaign."""
    from dario_app.modules.marketing_advanced.models import MarketingActivity
    
    query = select(MarketingActivity).where(MarketingActivity.campaign_id == campaign_id)
    result = await session.execute(query)
    activities = result.scalars().all()
    
    return {
        "campaign_id": campaign_id,
        "total_activities": len(activities),
        "activities": [
            {
                "id": a.id,
                "activity_code": a.activity_code,
                "name": a.name,
                "channel": a.channel,
                "status": a.status,
                "impressions": a.impressions,
                "conversions": a.conversions,
                "conversion_rate": a.conversion_rate
            }
            for a in activities
        ]
    }


# ============ Marketing List Endpoints ============

@router.post("/lists")
async def create_list(data: ListCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create marketing list."""
    from dario_app.modules.marketing_advanced.models import MarketingList
    
    mkt_list = MarketingList(
        organization_id=org_id,
        list_code=f"LIST-{uuid.uuid4().hex[:8].upper()}",
        name=data.name,
        list_type=data.list_type,
        description=data.description
    )
    session.add(mkt_list)
    await session.commit()
    return {"list_id": mkt_list.id, "list_code": mkt_list.list_code}


@router.get("/lists")
async def list_marketing_lists(session: AsyncSession = Depends(get_db), list_type: Optional[str] = None, org_id: str = "default"):
    """List marketing lists."""
    from dario_app.modules.marketing_advanced.models import MarketingList
    
    query = select(MarketingList).where(MarketingList.organization_id == org_id)
    if list_type:
        query = query.where(MarketingList.list_type == list_type)
    
    result = await session.execute(query)
    lists = result.scalars().all()
    
    return {
        "total": len(lists),
        "lists": [
            {
                "id": l.id,
                "list_code": l.list_code,
                "name": l.name,
                "list_type": l.list_type,
                "total_members": l.total_members,
                "active_members": l.active_members
            }
            for l in lists
        ]
    }


# ============ Email Template Endpoints ============

@router.post("/templates")
async def create_template(data: TemplateCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create email template."""
    from dario_app.modules.marketing_advanced.models import EmailTemplate
    
    template = EmailTemplate(
        organization_id=org_id,
        template_code=f"TMPL-{uuid.uuid4().hex[:8].upper()}",
        name=data.name,
        category=data.category,
        subject_line=data.subject_line,
        html_content=data.html_content
    )
    session.add(template)
    await session.commit()
    return {"template_id": template.id, "template_code": template.template_code}


@router.get("/templates")
async def list_templates(session: AsyncSession = Depends(get_db), category: Optional[str] = None, org_id: str = "default"):
    """List email templates."""
    from dario_app.modules.marketing_advanced.models import EmailTemplate
    
    query = select(EmailTemplate).where(EmailTemplate.organization_id == org_id)
    if category:
        query = query.where(EmailTemplate.category == category)
    
    result = await session.execute(query)
    templates = result.scalars().all()
    
    return {
        "total": len(templates),
        "templates": [
            {
                "id": t.id,
                "template_code": t.template_code,
                "name": t.name,
                "category": t.category,
                "subject_line": t.subject_line
            }
            for t in templates
        ]
    }


# ============ Customer Journey Endpoints ============

@router.post("/journeys")
async def create_journey(data: JourneyCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create customer journey."""
    from dario_app.modules.marketing_advanced.models import CustomerJourneyMap
    
    journey = CustomerJourneyMap(
        organization_id=org_id,
        journey_code=f"JRN-{uuid.uuid4().hex[:8].upper()}",
        name=data.name,
        journey_type=data.journey_type,
        description=data.description
    )
    session.add(journey)
    await session.commit()
    return {"journey_id": journey.id, "journey_code": journey.journey_code}


@router.get("/journeys")
async def list_journeys(session: AsyncSession = Depends(get_db), status: Optional[str] = None, org_id: str = "default"):
    """List customer journeys."""
    from dario_app.modules.marketing_advanced.models import CustomerJourneyMap
    
    query = select(CustomerJourneyMap).where(CustomerJourneyMap.organization_id == org_id)
    if status:
        query = query.where(CustomerJourneyMap.status == status)
    
    result = await session.execute(query)
    journeys = result.scalars().all()
    
    return {
        "total": len(journeys),
        "journeys": [
            {
                "id": j.id,
                "journey_code": j.journey_code,
                "name": j.name,
                "journey_type": j.journey_type,
                "status": j.status,
                "enrolled_contacts": j.enrolled_contacts,
                "completion_rate": f"{(j.completed_contacts / j.enrolled_contacts * 100) if j.enrolled_contacts > 0 else 0:.1f}%"
            }
            for j in journeys
        ]
    }


# ============ Lead Scoring Endpoints ============

@router.post("/lead-scoring-models")
async def create_scoring_model(data: LeadScoringCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create lead scoring model."""
    from dario_app.modules.marketing_advanced.models import LeadScoreModel
    
    model = LeadScoreModel(
        organization_id=org_id,
        model_code=f"LSM-{uuid.uuid4().hex[:8].upper()}",
        name=data.name,
        model_type=data.model_type,
        scoring_rules=data.scoring_rules
    )
    session.add(model)
    await session.commit()
    return {"model_id": model.id, "model_code": model.model_code}


@router.get("/lead-scoring-models")
async def list_scoring_models(session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """List lead scoring models."""
    from dario_app.modules.marketing_advanced.models import LeadScoreModel
    
    query = select(LeadScoreModel).where(LeadScoreModel.organization_id == org_id)
    result = await session.execute(query)
    models = result.scalars().all()
    
    return {
        "total": len(models),
        "models": [
            {
                "id": m.id,
                "model_code": m.model_code,
                "name": m.name,
                "model_type": m.model_type,
                "status": m.status,
                "model_accuracy": m.model_accuracy
            }
            for m in models
        ]
    }


# ============ Analytics Endpoints ============

@router.get("/analytics/campaign-performance")
async def get_campaign_performance(campaign_id: str, session: AsyncSession = Depends(get_db)):
    """Get campaign performance analytics."""
    from dario_app.modules.marketing_advanced.models import MarketingCampaign
    
    campaign = await session.get(MarketingCampaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign.name,
        "budget": campaign.budget,
        "actual_cost": campaign.actual_cost,
        "spend_percentage": f"{(campaign.actual_cost / campaign.budget * 100) if campaign.budget > 0 else 0:.1f}%",
        "reach": campaign.actual_reach,
        "leads_generated": campaign.total_leads,
        "qualified_leads": campaign.qualified_leads,
        "conversions": campaign.conversions,
        "conversion_rate": f"{campaign.roi_percent:.2f}%"
    }
