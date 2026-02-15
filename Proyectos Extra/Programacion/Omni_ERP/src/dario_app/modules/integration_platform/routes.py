"""
Integration Platform / API Management - Routes
Manage gateways, endpoints, throttling, keys, and integration flows.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db
from dario_app.modules.integration_platform.models import (
    ApiGateway,
    ApiEndpoint,
    ThrottlePolicy,
    ApiKey,
    IntegrationFlow,
)

router = APIRouter(prefix="/integration-platform", tags=["Integration Platform"])


# Gateways
@router.post("/gateways")
async def create_gateway(
    organization_id: int,
    name: str,
    base_url: str,
    authentication_mode: str = "APIKey",
    cors_policy: Optional[dict] = None,
    rate_limit_policy: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(ApiGateway.id)))
    count = result.scalar() or 0
    gateway_code = f"GW-{count + 1:04d}"

    gateway = ApiGateway(
        organization_id=organization_id,
        gateway_code=gateway_code,
        name=name,
        base_url=base_url,
        authentication_mode=authentication_mode,
        cors_policy=cors_policy or {},
        rate_limit_policy=rate_limit_policy or {},
    )
    db.add(gateway)
    await db.commit()
    await db.refresh(gateway)
    return gateway


@router.get("/gateways")
async def list_gateways(organization_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ApiGateway).where(ApiGateway.organization_id == organization_id))
    return result.scalars().all()


# Throttling
@router.post("/throttle-policies")
async def create_throttle_policy(
    organization_id: int,
    name: str,
    requests_per_minute: Optional[int] = None,
    burst_limit: Optional[int] = None,
    quota_per_day: Optional[int] = None,
    enforcement: str = "Hard",
    db: AsyncSession = Depends(get_db),
):
    policy = ThrottlePolicy(
        organization_id=organization_id,
        name=name,
        requests_per_minute=requests_per_minute,
        burst_limit=burst_limit,
        quota_per_day=quota_per_day,
        enforcement=enforcement,
    )
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    return policy


@router.get("/throttle-policies")
async def list_throttle_policies(organization_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ThrottlePolicy).where(ThrottlePolicy.organization_id == organization_id))
    return result.scalars().all()


# Endpoints
@router.post("/endpoints")
async def register_endpoint(
    organization_id: int,
    gateway_id: int,
    path: str,
    method: str,
    backend_url: str,
    throttling_policy_id: Optional[int] = None,
    auth_required: bool = True,
    db: AsyncSession = Depends(get_db),
):
    endpoint = ApiEndpoint(
        organization_id=organization_id,
        gateway_id=gateway_id,
        path=path,
        method=method,
        backend_url=backend_url,
        throttling_policy_id=throttling_policy_id,
        auth_required=auth_required,
    )
    db.add(endpoint)
    await db.commit()
    await db.refresh(endpoint)
    return endpoint


@router.get("/endpoints")
async def list_endpoints(organization_id: int, gateway_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(ApiEndpoint).where(ApiEndpoint.organization_id == organization_id)
    if gateway_id:
        query = query.where(ApiEndpoint.gateway_id == gateway_id)
    result = await db.execute(query)
    return result.scalars().all()


# API Keys
@router.post("/api-keys")
async def issue_api_key(
    organization_id: int,
    key_name: str,
    key_value: str,
    throttle_policy_id: Optional[int] = None,
    owner: Optional[str] = None,
    scopes: Optional[dict] = None,
    expires_at: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    api_key = ApiKey(
        organization_id=organization_id,
        key_name=key_name,
        key_value=key_value,
        throttle_policy_id=throttle_policy_id,
        owner=owner,
        scopes=scopes or {},
        expires_at=expires_at,
    )
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    return api_key


@router.patch("/api-keys/{key_id}/revoke")
async def revoke_api_key(key_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ApiKey).where(ApiKey.id == key_id))
    api_key = result.scalar_one_or_none()
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    api_key.status = "Revoked"
    api_key.revoked_at = datetime.utcnow()
    await db.commit()
    await db.refresh(api_key)
    return api_key


# Integration flows
@router.post("/flows")
async def create_flow(
    organization_id: int,
    name: str,
    connector_type: str,
    trigger_type: str,
    mapping: Optional[dict] = None,
    transformation: Optional[dict] = None,
    schedule: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(IntegrationFlow.id)))
    count = result.scalar() or 0
    flow_code = f"FLOW-{count + 1:05d}"

    flow = IntegrationFlow(
        organization_id=organization_id,
        flow_code=flow_code,
        name=name,
        connector_type=connector_type,
        trigger_type=trigger_type,
        mapping=mapping or {},
        transformation=transformation or {},
        schedule=schedule or {},
        status="Draft",
    )
    db.add(flow)
    await db.commit()
    await db.refresh(flow)
    return flow


@router.patch("/flows/{flow_id}/status")
async def update_flow_status(
    flow_id: int,
    status: str,
    last_run_status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(IntegrationFlow).where(IntegrationFlow.id == flow_id))
    flow = result.scalar_one_or_none()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")

    flow.status = status
    if last_run_status:
        flow.last_run_status = last_run_status
        flow.last_run_at = datetime.utcnow()

    await db.commit()
    await db.refresh(flow)
    return flow


# Analytics
@router.get("/analytics/gateway-usage")
async def gateway_usage(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Simple counts of endpoints and keys."""
    gateways = await db.execute(select(func.count(ApiGateway.id)).where(ApiGateway.organization_id == organization_id))
    endpoints = await db.execute(select(func.count(ApiEndpoint.id)).where(ApiEndpoint.organization_id == organization_id))
    keys = await db.execute(select(func.count(ApiKey.id)).where(ApiKey.organization_id == organization_id))
    return {
        "gateways": gateways.scalar() or 0,
        "endpoints": endpoints.scalar() or 0,
        "api_keys": keys.scalar() or 0,
    }
