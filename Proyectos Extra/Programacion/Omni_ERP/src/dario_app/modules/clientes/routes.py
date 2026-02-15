"""Clientes API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db

from .models import Cliente

router = APIRouter(prefix="/api/clientes", tags=["clientes"])


class ClienteCreate(BaseModel):
    nombre: str
    documento: str | None = None
    tipo_documento: str | None = None
    email: str | None = None
    telefono: str | None = None
    direccion: str | None = None


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    documento: str | None
    tipo_documento: str | None
    email: str
    telefono: str | None
    direccion: str | None
    puntos_lealtad: int
    nivel_lealtad: str
    total_compras: float
    activo: bool

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ClienteResponse])
async def list_clientes(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List all customers for the organization."""
    result = await db.execute(select(Cliente).where(Cliente.organization_id == org_id))
    return result.scalars().all()


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_cliente(
    cliente: ClienteCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new customer."""
    db_cliente = Cliente(**cliente.model_dump(), organization_id=org_id)
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def get_cliente(
    cliente_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get a customer by ID."""
    result = await db.execute(
        select(Cliente).where(Cliente.id == cliente_id, Cliente.organization_id == org_id)
    )
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
