"""Tenant isolation middleware and dependencies."""

from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core import settings
from dario_app.database import get_db
from dario_app.modules.usuarios.models import Permission, Role, RolePermission, UserRole, Usuario

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


async def get_current_user_org(request: Request) -> Optional[dict]:
    """Extract user and organization from JWT token in cookies or header."""
    token = request.cookies.get("access_token")

    # Also check Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        org_id: int = payload.get("org_id")
        email: str = payload.get("email")

        if user_id is None or org_id is None:
            return None

        return {"user_id": int(user_id), "org_id": org_id, "email": email}
    except JWTError:
        return None


async def require_auth(request: Request) -> dict:
    """Require authentication and return user context."""
    user_context = await get_current_user_org(request)

    if not user_context:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")

    return user_context


def get_org_id(user_context: dict = Depends(require_auth)) -> int:
    """Get organization ID from authenticated user context."""
    return user_context["org_id"]


def require_permission(permission_code: str):
    """Dependency factory to require a permission code or admin user."""

    async def dependency(
        user_context: dict = Depends(require_auth), db: AsyncSession = Depends(get_tenant_db)
    ) -> dict:
        # Admin bypass
        user_stmt = select(Usuario).where(Usuario.id == user_context["user_id"])
        user_res = await db.execute(user_stmt)
        usuario = user_res.scalar_one_or_none()
        if not usuario or not usuario.activo:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo")

        if usuario.es_admin:
            return user_context

        # Check if user has 'Admin' role (Dynamic Wildcard)
        admin_role_stmt = (
            select(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(
                Role.organization_id == user_context["org_id"],
                UserRole.usuario_id == user_context["user_id"],
                Role.nombre == "Admin"
            )
        )
        admin_role_res = await db.execute(admin_role_stmt)
        if admin_role_res.scalar_one_or_none():
            return user_context

        # Fetch all permission codes the user already has
        perms_stmt = (
            select(Permission.codigo)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(
                Role.organization_id == user_context["org_id"],
                UserRole.usuario_id == user_context["user_id"],
            )
        )
        perms_res = await db.execute(perms_stmt)
        user_perms = {row[0] for row in perms_res.all()}

        if permission_code not in user_perms:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

        # SoD enforcement
        from dario_app.modules.usuarios.models import SoDRule, SoDViolation

        sod_stmt = select(SoDRule).where(
            SoDRule.organization_id == user_context["org_id"],
            (SoDRule.perm_a == permission_code) | (SoDRule.perm_b == permission_code),
        )
        sod_res = await db.execute(sod_stmt)
        sod_rules = sod_res.scalars().all()

        for rule in sod_rules:
            other = rule.perm_b if rule.perm_a == permission_code else rule.perm_a
            if other in user_perms:
                violation = SoDViolation(
                    organization_id=user_context["org_id"],
                    user_id=user_context["user_id"],
                    attempted_permission=permission_code,
                    conflicting_permission=other,
                    rule_id=rule.id,
                    message=rule.description,
                )
                db.add(violation)
                await db.commit()
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Segregación de funciones: conflicto entre {permission_code} y {other}",
                )
        return user_context

    return dependency


async def get_tenant_db(org_id: int = Depends(get_org_id)):
    """Session en la base del tenant actual."""
    async for session in get_db(org_id):
        yield session
