"""Common FastAPI dependencies for database and org context."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db
from dario_app.database import get_db as base_get_db


async def get_db(org_id: int = Depends(get_org_id)) -> AsyncSession:
    """Return tenant DB session based on authenticated org_id."""
    async for session in base_get_db(org_id):
        yield session


def get_master_db():
    """Return master DB session (no tenant)."""
    return base_get_db(None)


# Re-export get_org_id to keep backwards compatibility
__all__ = ["get_db", "get_master_db", "get_org_id", "get_tenant_db"]
