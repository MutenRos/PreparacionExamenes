"""
Advanced Localization & Multi-currency - Models
Handles currencies, exchange rates, localization profiles, and language resources.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from dario_app.database import Base


class MultiCurrencySetting(Base):
    """Base currency and allowed currencies per organization."""
    __tablename__ = "loc_currency_settings"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, unique=True, nullable=False, index=True)

    base_currency = Column(String(10), default="USD")
    allowed_currencies = Column(JSON)
    rounding_policy = Column(String(50))  # Bankers, Up, Down
    decimal_places = Column(Integer, default=2)
    auto_update_rates = Column(Boolean, default=True)
    rate_provider = Column(String(100))  # ECB, XE, Custom

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CurrencyRate(Base):
    """Exchange rates by date."""
    __tablename__ = "loc_currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    base_currency = Column(String(10), nullable=False)
    target_currency = Column(String(10), nullable=False)
    rate = Column(Float, nullable=False)
    source = Column(String(100))
    effective_date = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)


class CurrencyConversionLog(Base):
    """Audit log of currency conversions performed."""
    __tablename__ = "loc_conversion_logs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    from_currency = Column(String(10), nullable=False)
    to_currency = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    converted_amount = Column(Float)
    rate_used = Column(Float)
    performed_at = Column(DateTime, default=datetime.utcnow)
    reference_type = Column(String(100))
    reference_id = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)


class LocalizationProfile(Base):
    """Regional settings per site or tenant."""
    __tablename__ = "loc_profiles"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    profile_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200))
    locale = Column(String(20), default="en-US")
    time_zone = Column(String(50), default="UTC")
    date_format = Column(String(50), default="YYYY-MM-DD")
    number_format = Column(String(50), default="1,234.56")
    currency_display = Column(String(50), default="symbol")  # symbol, code
    first_day_of_week = Column(String(10), default="Monday")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LanguageResource(Base):
    """Translated strings by locale."""
    __tablename__ = "loc_language_resources"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    key = Column(String(200), index=True)
    locale = Column(String(20), default="en-US", index=True)
    text = Column(String(500))
    context = Column(String(100))
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
