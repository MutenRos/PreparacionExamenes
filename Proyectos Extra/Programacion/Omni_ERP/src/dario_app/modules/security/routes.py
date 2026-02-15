"""Security & Compliance routes: SoD rules and GDPR tools."""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db, require_permission
from dario_app.modules.usuarios.models import Usuario, SoDRule, SoDViolation
from dario_app.services.audit_service import AuditService, AuditAction, AuditSeverity

router = APIRouter(prefix="/api/security", tags=["security"])


# ====== SoD Rules Management ======


class SoDRuleCreate(BaseModel):
    perm_a: str = Field(..., description="Permission code A")
    perm_b: str = Field(..., description="Permission code B")
    severity: str = Field("high", description="low|medium|high|critical")
    description: str | None = None


class SoDRuleResponse(BaseModel):
    id: int
    perm_a: str
    perm_b: str
    severity: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get(
    "/sod-rules",
    response_model=List[SoDRuleResponse],
    dependencies=[Depends(require_permission("security.admin"))],
)
async def list_sod_rules(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)):
    stmt = select(SoDRule).where(SoDRule.organization_id == org_id).order_by(SoDRule.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post(
    "/sod-rules",
    response_model=SoDRuleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("security.admin"))],
)
async def create_sod_rule(payload: SoDRuleCreate, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)):
    if payload.perm_a == payload.perm_b:
        raise HTTPException(status_code=400, detail="perm_a y perm_b deben ser distintos")

    existing = await db.execute(
        select(SoDRule).where(
            SoDRule.organization_id == org_id,
            SoDRule.perm_a == payload.perm_a,
            SoDRule.perm_b == payload.perm_b,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Regla ya existe")

    rule = SoDRule(
        organization_id=org_id,
        perm_a=payload.perm_a,
        perm_b=payload.perm_b,
        severity=payload.severity,
        description=payload.description,
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.delete(
    "/sod-rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("security.admin"))],
)
async def delete_sod_rule(rule_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)):
    stmt = select(SoDRule).where(SoDRule.id == rule_id, SoDRule.organization_id == org_id)
    res = await db.execute(stmt)
    rule = res.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    await db.execute(delete(SoDRule).where(SoDRule.id == rule_id))
    await db.commit()


# ====== SoD Violations ======


class SoDViolationResponse(BaseModel):
    id: int
    user_id: int
    attempted_permission: str
    conflicting_permission: str
    rule_id: int | None
    message: str | None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get(
    "/sod-violations",
    response_model=List[SoDViolationResponse],
    dependencies=[Depends(require_permission("security.admin"))],
)
async def list_sod_violations(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)):
    stmt = (
        select(SoDViolation)
        .where(SoDViolation.organization_id == org_id)
        .order_by(SoDViolation.created_at.desc())
        .limit(200)
    )
    res = await db.execute(stmt)
    return res.scalars().all()


# ====== GDPR Tools ======


class GDPRExportResponse(BaseModel):
    id: int
    username: str
    email: str
    email_personal: str | None
    telefono: str | None
    dni: str | None
    iban: str | None
    nombre: str | None
    apellidos: str | None
    nombre_completo: str | None
    activo: bool
    anonimizado_en: datetime | None

    class Config:
        from_attributes = True


@router.get(
    "/gdpr/users/{user_id}/export",
    response_model=GDPRExportResponse,
    dependencies=[Depends(require_permission("security.gdpr"))],
)
async def gdpr_export_user(user_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)):
    user_res = await db.execute(
        select(Usuario).where(Usuario.id == user_id, Usuario.organization_id == org_id)
    )
    user = user_res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


class GDPRAnonymizeResponse(BaseModel):
    id: int
    anonimizado_en: datetime | None
    activo: bool

    class Config:
        from_attributes = True


@router.post(
    "/gdpr/users/{user_id}/anonymize",
    response_model=GDPRAnonymizeResponse,
    dependencies=[Depends(require_permission("security.gdpr"))],
)
async def gdpr_anonymize_user(user_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)):
    user_res = await db.execute(
        select(Usuario).where(Usuario.id == user_id, Usuario.organization_id == org_id)
    )
    user = user_res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    timestamp = datetime.utcnow()
    user.email = f"anon-{user.id}@example.com"
    user.email_personal = None
    user.telefono = None
    user.dni = None
    user.iban = None
    user.nombre = "ANON"
    user.apellidos = "YMIZED"
    user.nombre_completo = f"Anon {user.id}"
    user.activo = False
    user.anonimizado_en = timestamp

    await db.commit()
    await AuditService.log(
        db=db,
        organization_id=org_id,
        action=AuditAction.UPDATE,
        resource_type="usuario",
        resource_id=str(user.id),
        user_id=None,
        user_email=None,
        description="GDPR anonymize user",
        severity=AuditSeverity.CRITICAL,
        is_sensitive=True,
    )
    return user