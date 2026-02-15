"""Usuarios API routes."""

from typing import List
import secrets
import string
import re

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission
from dario_app.database import get_db
from dario_app.modules.tenants.models import Organization

from .models import Permission, Role, RolePermission, UserRole, Usuario

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


def get_org_id() -> int:
    """Get organization ID - for now hardcoded to 1."""
    return 1


async def get_tenant_db_local(org_id: int = Depends(get_org_id)):
    """Session en la base del tenant actual."""
    async for session in get_db(org_id):
        yield session


def generar_username(nombre_completo: str) -> str:
    """Generate username from full name: 'Juan Pérez' -> 'juan.perez'"""
    # Normalize: lowercase, remove accents
    nombre = re.sub(r'[áéíóú]', lambda m: 'aeiou'['áéíóú'.index(m.group())], nombre_completo.lower())
    # Replace spaces with dots
    username = re.sub(r'\s+', '.', nombre.strip())
    # Remove invalid chars
    username = re.sub(r'[^a-z0-9.]', '', username)
    return username


def generar_email_empresa(nombre_completo: str, dominio: str = "empresa.com") -> str:
    """Generate company email: 'Juan Pérez' -> 'juan.perez@empresa.com'"""
    username = generar_username(nombre_completo)
    return f"{username}@{dominio}"


def generar_contraseña(longitud: int = 12) -> str:
    """Generate secure random password."""
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))


class UsuarioCreate(BaseModel):
    """Create usuario with auto-generated username, email_empresa, and password."""
    nombre: str
    apellidos: str
    email_personal: EmailStr
    telefono: str | None = None
    es_admin: bool = False
    dni: str | None = None
    iban: str | None = None


class UsuarioCreateResponse(BaseModel):
    """Response with auto-generated credentials."""
    id: int
    username: str
    email_empresa: str
    password_temporal: str  # Show generated password only on creation
    nombre: str
    apellidos: str
    nombre_completo: str
    email_personal: str
    telefono: str | None
    activo: bool
    es_admin: bool
    dni: str | None
    iban: str | None

    class Config:
        from_attributes = True


class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
    nombre_completo: str | None
    activo: bool
    es_admin: bool

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    nombre: str
    descripcion: str | None = None


class RoleResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    es_sistema: bool

    class Config:
        from_attributes = True


class PermissionCreate(BaseModel):
    codigo: str
    nombre: str
    descripcion: str | None = None


class PermissionResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    descripcion: str | None

    class Config:
        from_attributes = True


class AssignRoleRequest(BaseModel):
    role_id: int


class AssignPermissionsRequest(BaseModel):
    permission_ids: List[int]


@router.get("/", response_model=List[UsuarioResponse])
async def list_usuarios(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db_local)
):
    """List all users."""
    result = await db.execute(select(Usuario).where(Usuario.organization_id == org_id))
    return result.scalars().all()


@router.post("/", response_model=UsuarioCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario: UsuarioCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db_local),
):
    """Create a new user with auto-generated credentials."""
    # Fetch organization to get domain
    org_result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = org_result.scalar_one_or_none()
    
    domain = "empresa.com"
    if org:
        # Use slug for domain, e.g. my-company.com
        domain = f"{org.slug}.com"

    # Build full name, auto-generate username, email_empresa, and password
    nombre_completo = f"{usuario.nombre} {usuario.apellidos}".strip()
    username = generar_username(nombre_completo)
    email_empresa = generar_email_empresa(nombre_completo, domain)
    password_temporal = generar_contraseña()
    
    # Hash password
    password_bytes = password_temporal.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    # Check if username already exists
    existing = await db.execute(
        select(Usuario).where(
            Usuario.username == username,
            Usuario.organization_id == org_id
        )
    )
    if existing.scalar_one_or_none():
        # Add number suffix if username exists
        counter = 1
        while True:
            new_username = f"{username}{counter}"
            existing = await db.execute(
                select(Usuario).where(
                    Usuario.username == new_username,
                    Usuario.organization_id == org_id
                )
            )
            if not existing.scalar_one_or_none():
                username = new_username
                break
            counter += 1

    # Check DNI uniqueness (if provided)
    if usuario.dni:
        existing_dni = await db.execute(
            select(Usuario).where(
                Usuario.dni == usuario.dni,
                Usuario.organization_id == org_id,
            )
        )
        if existing_dni.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="El DNI ya está registrado")

    # Normalize and basic-validate IBAN (if provided)
    iban_normalizado = None
    if usuario.iban:
        iban_normalizado = re.sub(r"\s+", "", usuario.iban).upper()
        if not validar_iban(iban_normalizado):
            raise HTTPException(status_code=400, detail="IBAN inválido")

    db_usuario = Usuario(
        username=username,
        email=email_empresa,
        hashed_password=hashed_password,
        nombre=usuario.nombre,
        apellidos=usuario.apellidos,
        nombre_completo=nombre_completo,
        email_personal=usuario.email_personal,
        telefono=usuario.telefono,
        dni=usuario.dni,
        iban=iban_normalizado,
        es_admin=usuario.es_admin,
        organization_id=org_id,
    )
    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)
    
    # Return with temporary password (only shown on creation)
    return {
        "id": db_usuario.id,
        "username": username,
        "email_empresa": email_empresa,
        "password_temporal": password_temporal,
        "nombre": db_usuario.nombre,
        "apellidos": db_usuario.apellidos,
        "nombre_completo": db_usuario.nombre_completo,
        "email_personal": db_usuario.email_personal,
        "telefono": db_usuario.telefono,
        "dni": db_usuario.dni,
        "iban": db_usuario.iban,
        "activo": db_usuario.activo,
        "es_admin": db_usuario.es_admin,
    }

def validar_iban(iban: str) -> bool:
    """Validate IBAN using ISO 13616: move first 4 chars to end, convert letters to numbers (A=10..Z=35), then mod 97 == 1."""
    iban_norm = re.sub(r"\s+", "", iban).upper()
    # Basic length and country/check digits
    if not re.fullmatch(r"^[A-Z]{2}\d{2}[A-Z0-9]{10,30}$", iban_norm):
        return False
    rearranged = iban_norm[4:] + iban_norm[:4]
    # Convert letters to digits
    digits = []
    for ch in rearranged:
        if ch.isdigit():
            digits.append(ch)
        else:
            digits.append(str(ord(ch) - 55))  # A->10 ... Z->35
    num_str = "".join(digits)
    # Compute mod 97 in chunks to avoid big ints
    remainder = 0
    for i in range(0, len(num_str), 9):
        chunk = str(remainder) + num_str[i:i+9]
        remainder = int(chunk) % 97
    return remainder == 1


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db_local)
):
    """Get a user by ID."""
    result = await db.execute(
        select(Usuario).where(Usuario.id == usuario_id, Usuario.organization_id == org_id)
    )
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# ----- Roles -----


@router.get("/roles", response_model=List[RoleResponse])
async def list_roles(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db_local)):
    result = await db.execute(select(Role).where(Role.organization_id == org_id))
    return result.scalars().all()


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db_local),
    _=Depends(require_permission("manage_roles")),
):
    # Prevent duplicate name in org
    exists = await db.execute(
        select(Role).where(Role.organization_id == org_id, Role.nombre == role.nombre)
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El rol ya existe")

    db_role = Role(
        organization_id=org_id,
        nombre=role.nombre,
        descripcion=role.descripcion,
    )
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


# ----- Permisos -----


@router.get("/permisos", response_model=List[PermissionResponse])
async def list_permissions(db: AsyncSession = Depends(get_tenant_db_local)):
    result = await db.execute(select(Permission))
    return result.scalars().all()


@router.post("/permisos", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permiso: PermissionCreate,
    db: AsyncSession = Depends(get_tenant_db_local),
    _=Depends(require_permission("manage_roles")),
):
    existing = await db.execute(select(Permission).where(Permission.codigo == permiso.codigo))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El permiso ya existe")

    db_perm = Permission(
        codigo=permiso.codigo,
        nombre=permiso.nombre,
        descripcion=permiso.descripcion,
    )
    db.add(db_perm)
    await db.commit()
    await db.refresh(db_perm)
    return db_perm


# ----- Asignaciones -----


@router.post("/{usuario_id}/roles", status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_to_user(
    usuario_id: int,
    payload: AssignRoleRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db_local),
    _=Depends(require_permission("manage_roles")),
):
    # Ensure user belongs to org
    user_res = await db.execute(
        select(Usuario).where(Usuario.id == usuario_id, Usuario.organization_id == org_id)
    )
    user = user_res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    role_res = await db.execute(
        select(Role).where(Role.id == payload.role_id, Role.organization_id == org_id)
    )
    role = role_res.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    exists = await db.execute(
        select(UserRole).where(UserRole.usuario_id == usuario_id, UserRole.role_id == role.id)
    )
    if exists.scalar_one_or_none():
        return

    db.add(UserRole(usuario_id=usuario_id, role_id=role.id))
    await db.commit()


@router.get("/{usuario_id}/roles", response_model=List[RoleResponse])
async def list_user_roles(
    usuario_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db_local),
    _=Depends(require_permission("view_users")),
):
    stmt = (
        select(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.usuario_id == usuario_id, Role.organization_id == org_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/roles/{role_id}/permisos", status_code=status.HTTP_204_NO_CONTENT)
async def assign_permissions_to_role(
    role_id: int,
    request: AssignPermissionsRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db_local),
    _=Depends(require_permission("manage_roles")),
):
    """Assign multiple permissions to a role."""
    role_res = await db.execute(
        select(Role).where(Role.id == role_id, Role.organization_id == org_id)
    )
    role = role_res.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    # Eliminar permisos actuales
    await db.execute(delete(RolePermission).where(RolePermission.role_id == role_id))

    # Agregar nuevos permisos
    for perm_id in request.permission_ids:
        db.add(RolePermission(role_id=role.id, permission_id=perm_id))

    await db.commit()


@router.get("/roles/{role_id}")
async def get_role_with_permissions(
    role_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db_local)
):
    """Get a role with its permissions."""
    role_res = await db.execute(
        select(Role).where(Role.id == role_id, Role.organization_id == org_id)
    )
    role = role_res.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    # Get permissions for this role
    perms_res = await db.execute(
        select(Permission)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .where(RolePermission.role_id == role_id)
    )
    permissions = perms_res.scalars().all()

    return {
        "id": role.id,
        "nombre": role.nombre,
        "descripcion": role.descripcion,
        "es_sistema": role.es_sistema,
        "permissions": [
            {"id": p.id, "codigo": p.codigo, "nombre": p.nombre, "descripcion": p.descripcion}
            for p in permissions
        ],
    }
