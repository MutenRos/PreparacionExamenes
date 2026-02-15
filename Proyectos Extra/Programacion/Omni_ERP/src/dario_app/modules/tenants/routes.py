"""Organization/Tenant API routes."""

from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from dario_app.core.auth import get_org_id, require_auth
from dario_app.database import ORG_DB_DIR, create_tenant_db, get_db

from .models import Organization

router = APIRouter(prefix="/api/organization", tags=["organization"])


class OrganizationFiscalData(BaseModel):
    """Fiscal/legal data for organization."""

    razon_social: str
    ruc_numero: str
    ruc_digito: Optional[str] = None
    direccion: str
    ciudad: str
    provincia: str
    codigo_postal: str
    pais: str = "Perú"
    regimen_tributario: Optional[str] = None
    telefono: Optional[str] = None
    website: Optional[str] = None

    @field_validator("ruc_numero")
    @classmethod
    def validate_ruc(cls, v):
        if not v or len(v) < 8:
            raise ValueError("RUC debe tener al menos 8 caracteres")
        return v

    @field_validator("razon_social", "direccion", "ciudad", "provincia", "codigo_postal")
    @classmethod
    def validate_required(cls, v):
        if not v or not v.strip():
            raise ValueError("Este campo es obligatorio")
        return v.strip()


class OrganizationResponse(BaseModel):
    """Organization response."""

    id: int
    nombre: str
    email: str
    plan: str
    estado: str
    razon_social: Optional[str]
    ruc_numero: Optional[str]
    datos_fiscales_completos: bool

    class Config:
        from_attributes = True


class TenantDbInfo(BaseModel):
    org_id: int
    path: str
    exists: bool
    size_bytes: int


# === Module enablement & workflow config ===

DEFAULT_MODULES = [
    "ventas",
    "pos",
    "produccion",
    "compras",
    "oficina_tecnica",
    "almacen",
    "recepcion",
]


class ModulesConfigResponse(BaseModel):
    enabled_modules: list[str]
    available_modules: list[str]


class ModulesConfigRequest(BaseModel):
    enabled_modules: list[str]

    @field_validator("enabled_modules")
    @classmethod
    def validate_modules(cls, v):
        allowed = set(DEFAULT_MODULES)
        for m in v:
            if m not in allowed:
                raise ValueError(f"Módulo desconocido: {m}")
        return v


class WorkflowConfigResponse(BaseModel):
    workflow: str  # Mermaid or JSON string representation
    workflow_graph: Optional[Dict[str, Any]] = None  # Scratch-like graph structure


class WorkflowConfigRequest(BaseModel):
    workflow: str
    workflow_graph: Optional[Dict[str, Any]] = None


@router.get("/", response_model=OrganizationResponse)
async def get_organization(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_db)):
    """Get organization information."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    return organization


@router.put("/fiscal-data", response_model=OrganizationResponse)
async def update_fiscal_data(
    fiscal_data: OrganizationFiscalData,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
):
    """Update organization fiscal/legal data (master + tenant)."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    # Update master fiscal data
    organization.razon_social = fiscal_data.razon_social
    organization.ruc_numero = fiscal_data.ruc_numero
    organization.ruc_digito = fiscal_data.ruc_digito
    organization.direccion = fiscal_data.direccion
    organization.ciudad = fiscal_data.ciudad
    organization.provincia = fiscal_data.provincia
    organization.codigo_postal = fiscal_data.codigo_postal
    organization.pais = fiscal_data.pais
    organization.regimen_tributario = fiscal_data.regimen_tributario
    organization.website = fiscal_data.website

    if fiscal_data.telefono:
        organization.telefono = fiscal_data.telefono

    organization.datos_fiscales_completos = True
    organization.actualizado_en = datetime.utcnow()

    await db.commit()
    await db.refresh(organization)

    # Also update tenant DB clone for consistency
    try:
        async for tenant_db in get_db(org_id):
            t_res = await tenant_db.execute(select(Organization).where(Organization.id == org_id))
            t_org = t_res.scalar_one_or_none()
            if t_org:
                t_org.razon_social = organization.razon_social
                t_org.ruc_numero = organization.ruc_numero
                t_org.ruc_digito = organization.ruc_digito
                t_org.direccion = organization.direccion
                t_org.ciudad = organization.ciudad
                t_org.provincia = organization.provincia
                t_org.codigo_postal = organization.codigo_postal
                t_org.pais = organization.pais
                t_org.regimen_tributario = organization.regimen_tributario
                t_org.website = organization.website
                t_org.telefono = organization.telefono
                t_org.datos_fiscales_completos = True
                t_org.actualizado_en = datetime.utcnow()
                await tenant_db.commit()
    except Exception as e:
        # Non-fatal if tenant sync fails; master is source of truth
        print(f"[WARN] Tenant fiscal sync failed for org {org_id}: {e}")

    return organization


@router.get("/can-upgrade")
async def can_upgrade_plan(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_db)):
    """Check if organization can upgrade to paid plan."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    return {
        "can_upgrade": organization.datos_fiscales_completos,
        "reason": (
            None
            if organization.datos_fiscales_completos
            else "Complete los datos fiscales de su empresa"
        ),
        "datos_fiscales_completos": organization.datos_fiscales_completos,
    }


@router.get("/modules-config", response_model=ModulesConfigResponse)
async def get_modules_config(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_db)):
    """Return enabled modules for the organization."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    enabled_modules = DEFAULT_MODULES
    try:
        if organization.configuracion:
            cfg = json.loads(organization.configuracion)
            enabled_modules = cfg.get("enabled_modules", enabled_modules)
    except Exception:
        # If parsing fails, fall back to defaults
        enabled_modules = DEFAULT_MODULES

    return ModulesConfigResponse(enabled_modules=enabled_modules, available_modules=DEFAULT_MODULES)


@router.put("/modules-config", response_model=ModulesConfigResponse)
async def update_modules_config(
    payload: ModulesConfigRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
):
    """Update enabled modules for the organization."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    cfg = {}
    try:
        if organization.configuracion:
            cfg = json.loads(organization.configuracion)
    except Exception:
        cfg = {}

    cfg["enabled_modules"] = payload.enabled_modules
    organization.configuracion = json.dumps(cfg, ensure_ascii=False)
    organization.actualizado_en = datetime.utcnow()
    await db.commit()
    await db.refresh(organization)

    return ModulesConfigResponse(enabled_modules=payload.enabled_modules, available_modules=DEFAULT_MODULES)


DEFAULT_WORKFLOW = """
flowchart TD
    A[Venta/POS aprobada] --> B{Generar OP}
    B --> C[Asignar Sección]
    C --> D[Aceptación Supervisor]
    D --> E[Adquisición de Materiales]
    E --> F[En Proceso]
    F --> G[Calidad]
    G --> H[Completada]
""".strip()


@router.get("/workflow-config", response_model=WorkflowConfigResponse)
async def get_workflow_config(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_db)):
    """Return visual workflow (Mermaid) and structured graph for the organization."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    workflow = DEFAULT_WORKFLOW
    workflow_graph: Optional[Dict[str, Any]] = None
    try:
        if organization.configuracion:
            cfg = json.loads(organization.configuracion)
            workflow = cfg.get("workflow", workflow)
            workflow_graph = cfg.get("workflow_graph")
    except Exception:
        workflow = DEFAULT_WORKFLOW
        workflow_graph = None

    return WorkflowConfigResponse(workflow=workflow, workflow_graph=workflow_graph)


@router.put("/workflow-config", response_model=WorkflowConfigResponse)
async def update_workflow_config(
    payload: WorkflowConfigRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
):
    """Update visual workflow (Mermaid) and structured graph for the organization."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    cfg = {}
    try:
        if organization.configuracion:
            cfg = json.loads(organization.configuracion)
    except Exception:
        cfg = {}

    cfg["workflow"] = payload.workflow
    if payload.workflow_graph is not None:
        cfg["workflow_graph"] = payload.workflow_graph
    organization.configuracion = json.dumps(cfg, ensure_ascii=False)
    organization.actualizado_en = datetime.utcnow()
    await db.commit()
    await db.refresh(organization)

    return WorkflowConfigResponse(workflow=payload.workflow, workflow_graph=payload.workflow_graph)


@router.post("/{org_id}/provision-db", response_model=TenantDbInfo)
async def provision_tenant_db(org_id: int, user_ctx: dict = Depends(require_auth)):
    """Crear la base de datos del tenant (idempotente)."""
    path = await create_tenant_db(org_id)
    p = Path(path)
    return TenantDbInfo(
        org_id=org_id,
        path=str(p),
        exists=p.exists(),
        size_bytes=p.stat().st_size if p.exists() else 0,
    )


@router.get("/databases", response_model=list[TenantDbInfo])
async def list_tenant_dbs(user_ctx: dict = Depends(require_auth)):
    """Listar bases de datos de tenants (archivos en org_dbs)."""
    results = []
    if ORG_DB_DIR.exists():
        for f in ORG_DB_DIR.glob("org_*.db"):
            try:
                org_id = int(f.stem.split("_")[1])
            except Exception:
                continue
            results.append(
                TenantDbInfo(
                    org_id=org_id,
                    path=str(f),
                    exists=f.exists(),
                    size_bytes=f.stat().st_size if f.exists() else 0,
                )
            )
    return results


@router.get("/{org_id}/db-health", response_model=TenantDbInfo)
async def tenant_db_health(org_id: int, user_ctx: dict = Depends(require_auth)):
    """Verificar existencia y tamaño de la base de un tenant."""
    path = ORG_DB_DIR / f"org_{org_id}.db"
    return TenantDbInfo(
        org_id=org_id,
        path=str(path),
        exists=path.exists(),
        size_bytes=path.stat().st_size if path.exists() else 0,
    )
