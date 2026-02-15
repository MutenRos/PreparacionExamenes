"""
Integration Platform / API Management - Models
Handles gateways, endpoints, keys, throttling, and integration flows.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from dario_app.database import Base


class ApiGateway(Base):
    """API gateway configuration."""
    __tablename__ = "ip_gateways"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    gateway_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    base_url = Column(String(255))
    authentication_mode = Column(String(50))  # APIKey, OAuth2, JWT
    cors_policy = Column(JSON)
    rate_limit_policy = Column(JSON)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    endpoints = relationship("ApiEndpoint", back_populates="gateway", cascade="all, delete-orphan")


class ApiEndpoint(Base):
    """Managed API endpoint exposed via gateway."""
    __tablename__ = "ip_endpoints"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    gateway_id = Column(Integer, ForeignKey("ip_gateways.id"))

    path = Column(String(200), nullable=False)
    method = Column(String(20), nullable=False)
    backend_url = Column(String(255), nullable=False)
    auth_required = Column(Boolean, default=True)
    transform_policy = Column(JSON)
    cache_policy = Column(JSON)
    throttling_policy_id = Column(Integer, ForeignKey("ip_throttle_policies.id"))
    status = Column(String(50), default="Active")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    gateway = relationship("ApiGateway", back_populates="endpoints")
    throttling_policy = relationship("ThrottlePolicy", back_populates="endpoints")


class ThrottlePolicy(Base):
    """Throttling and quota policies."""
    __tablename__ = "ip_throttle_policies"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    name = Column(String(200), nullable=False)
    requests_per_minute = Column(Integer)
    burst_limit = Column(Integer)
    quota_per_day = Column(Integer)
    enforcement = Column(String(50), default="Hard")  # Hard, Soft
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    endpoints = relationship("ApiEndpoint", back_populates="throttling_policy")
    api_keys = relationship("ApiKey", back_populates="throttle_policy")


class ApiKey(Base):
    """API keys and client applications."""
    __tablename__ = "ip_api_keys"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    throttle_policy_id = Column(Integer, ForeignKey("ip_throttle_policies.id"))

    key_name = Column(String(200), nullable=False)
    key_value = Column(String(255), unique=True, nullable=False, index=True)
    owner = Column(String(200))
    scopes = Column(JSON)
    expires_at = Column(DateTime)
    status = Column(String(50), default="Active")

    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime)

    throttle_policy = relationship("ThrottlePolicy", back_populates="api_keys")


class IntegrationFlow(Base):
    """Integration workflows and connectors."""
    __tablename__ = "ip_integration_flows"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    flow_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200))
    connector_type = Column(String(100))  # SAP, Salesforce, Dynamics, Custom
    trigger_type = Column(String(50))  # Webhook, Schedule, Event
    mapping = Column(JSON)  # field mappings
    transformation = Column(JSON)
    schedule = Column(JSON)
    status = Column(String(50), default="Draft")
    last_run_at = Column(DateTime)
    last_run_status = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
