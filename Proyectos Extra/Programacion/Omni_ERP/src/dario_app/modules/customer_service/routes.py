"""Customer Service routes - Cases, Knowledge Base, Entitlements."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import Case, CaseComment, CSKnowledgeArticle, Entitlement

router = APIRouter(prefix="/api/customer-service", tags=["Customer Service"])


# Schemas

class CaseCreate(BaseModel):
    title: str
    descripcion: Optional[str] = None
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    priority: str = "normal"
    severity: str = "minor"
    category: Optional[str] = None
    product: Optional[str] = None


class CaseUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_user_id: Optional[int] = None
    assigned_to_name: Optional[str] = None


class CommentCreate(BaseModel):
    comment: str
    is_internal: bool = False


class KBArticleCreate(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    category: Optional[str] = None
    keywords: Optional[str] = None


class EntitlementCreate(BaseModel):
    name: str
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    start_date: str
    end_date: str
    entitlement_type: str = "incidents"
    total_incidents: Optional[int] = None
    total_hours: Optional[float] = None


# Cases

@router.post("/cases")
async def create_case(
    payload: CaseCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.cases.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate case number
    stmt = select(Case).where(Case.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    case_number = f"CASE-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    case = Case(
        organization_id=org_id,
        case_number=case_number,
        **payload.model_dump()
    )
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case


@router.get("/cases")
async def list_cases(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.cases.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Case).where(Case.organization_id == org_id)
    if status:
        query = query.where(Case.status == status)
    if priority:
        query = query.where(Case.priority == priority)
    if assigned_to:
        query = query.where(Case.assigned_to_user_id == assigned_to)
    query = query.order_by(Case.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/cases/{case_id}")
async def get_case(
    case_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.cases.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Case).where(Case.id == case_id, Case.organization_id == org_id)
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.patch("/cases/{case_id}")
async def update_case(
    case_id: int,
    payload: CaseUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.cases.update")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Case).where(Case.id == case_id, Case.organization_id == org_id)
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(case, field, value)
    
    if payload.status == "resolved" and not case.resolved_at:
        case.resolved_at = datetime.utcnow()
    if payload.status == "closed" and not case.closed_at:
        case.closed_at = datetime.utcnow()
    
    case.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(case)
    return case


@router.post("/cases/{case_id}/escalate")
async def escalate_case(
    case_id: int,
    escalated_to_name: str,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.cases.escalate")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Case).where(Case.id == case_id, Case.organization_id == org_id)
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case.escalated = True
    case.escalated_at = datetime.utcnow()
    case.escalated_to_name = escalated_to_name
    case.priority = "urgent"
    await db.commit()
    await db.refresh(case)
    return case


# Case Comments

@router.post("/cases/{case_id}/comments")
async def add_comment(
    case_id: int,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.cases.comment")),
    org_id: int = Depends(get_org_id),
):
    comment = CaseComment(
        organization_id=org_id,
        case_id=case_id,
        comment=payload.comment,
        is_internal=payload.is_internal,
        author_user_id=user.id,
        author_name=user.nombre_completo,
    )
    db.add(comment)
    
    # Update first_response_at if this is the first comment
    stmt = select(Case).where(Case.id == case_id, Case.organization_id == org_id)
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if case and not case.first_response_at:
        case.first_response_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("/cases/{case_id}/comments")
async def list_comments(
    case_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.cases.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CaseComment).where(
        CaseComment.organization_id == org_id,
        CaseComment.case_id == case_id
    ).order_by(CaseComment.created_at)
    result = await db.execute(query)
    return result.scalars().all()


# Knowledge Base

@router.post("/kb/articles")
async def create_article(
    payload: KBArticleCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.kb.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate article number
    stmt = select(CSKnowledgeArticle).where(CSCSKnowledgeArticle.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    article_number = f"KB-{count + 1:05d}"
    
    article = CSKnowledgeArticle(
        organization_id=org_id,
        article_number=article_number,
        author_user_id=user.id,
        author_name=user.nombre_completo,
        **payload.model_dump()
    )
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article


@router.get("/kb/articles")
async def list_articles(
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.kb.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CSKnowledgeArticle).where(CSCSKnowledgeArticle.organization_id == org_id)
    if status:
        query = query.where(CSCSKnowledgeArticle.status == status)
    if category:
        query = query.where(CSCSKnowledgeArticle.category == category)
    if search:
        query = query.where(
            or_(
                CSCSKnowledgeArticle.title.ilike(f"%{search}%"),
                CSCSKnowledgeArticle.content.ilike(f"%{search}%"),
                CSCSKnowledgeArticle.keywords.ilike(f"%{search}%"),
            )
        )
    query = query.order_by(CSCSKnowledgeArticle.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/kb/articles/{article_id}/publish")
async def publish_article(
    article_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.kb.publish")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(CSKnowledgeArticle).where(
        CSCSKnowledgeArticle.id == article_id,
        CSCSKnowledgeArticle.organization_id == org_id
    )
    result = await db.execute(stmt)
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article.status = "published"
    article.published_at = datetime.utcnow()
    await db.commit()
    await db.refresh(article)
    return article


@router.post("/kb/articles/{article_id}/feedback")
async def article_feedback(
    article_id: int,
    helpful: bool,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    stmt = select(CSKnowledgeArticle).where(
        CSCSKnowledgeArticle.id == article_id,
        CSCSKnowledgeArticle.organization_id == org_id
    )
    result = await db.execute(stmt)
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if helpful:
        article.helpful_count += 1
    else:
        article.not_helpful_count += 1
    
    await db.commit()
    return {"helpful_count": article.helpful_count, "not_helpful_count": article.not_helpful_count}


# Entitlements

@router.post("/entitlements")
async def create_entitlement(
    payload: EntitlementCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.entitlements.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate entitlement number
    stmt = select(Entitlement).where(Entitlement.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    entitlement_number = f"ENT-{datetime.now().strftime('%Y')}-{count + 1:04d}"
    
    entitlement = Entitlement(
        organization_id=org_id,
        entitlement_number=entitlement_number,
        **payload.model_dump()
    )
    db.add(entitlement)
    await db.commit()
    await db.refresh(entitlement)
    return entitlement


@router.get("/entitlements")
async def list_entitlements(
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.entitlements.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Entitlement).where(Entitlement.organization_id == org_id)
    if customer_id:
        query = query.where(Entitlement.customer_id == customer_id)
    if status:
        query = query.where(Entitlement.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/entitlements/{entitlement_id}")
async def get_entitlement(
    entitlement_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_service.entitlements.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Entitlement).where(
        Entitlement.id == entitlement_id,
        Entitlement.organization_id == org_id
    )
    result = await db.execute(stmt)
    entitlement = result.scalar_one_or_none()
    if not entitlement:
        raise HTTPException(status_code=404, detail="Entitlement not found")
    return entitlement
