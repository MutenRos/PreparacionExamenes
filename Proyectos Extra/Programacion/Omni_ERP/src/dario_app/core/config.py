"""Core configuration and settings."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "OmniERP"
    version: str = "2.0.0"  # Enterprise Edition
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = True
    secret_key: str = "dev-secret-key-change-in-production"
    
    # Redis cache (optional)
    redis_url: Optional[str] = None  # redis://localhost:6379/0
    
    # Database
    database_encryption_key: Optional[str] = None
    
    # Security
    cors_origins: str = "*"  # Comma-separated list in production
    session_timeout_minutes: int = 60
    max_login_attempts: int = 5
    
    # Features
    enable_2fa: bool = True
    enable_analytics: bool = True
    enable_webhooks: bool = True
    enable_graphql: bool = True
    
    # Integrations
    stripe_api_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from: str = "noreply@omnierp.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
