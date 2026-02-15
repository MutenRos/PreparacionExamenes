"""
Advanced Localization & Multi-currency - Routes
Manage currency settings, rates, conversions, and localization profiles.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db
from dario_app.modules.localization.models import (
    MultiCurrencySetting,
    CurrencyRate,
    CurrencyConversionLog,
    LocalizationProfile,
    LanguageResource,
)

router = APIRouter(prefix="/localization", tags=["Localization & Currency"])


# Currency settings
@router.post("/currency/settings")
async def upsert_currency_settings(
    organization_id: int,
    base_currency: str = "USD",
    allowed_currencies: Optional[list] = None,
    rounding_policy: Optional[str] = None,
    decimal_places: int = 2,
    auto_update_rates: bool = True,
    rate_provider: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MultiCurrencySetting).where(MultiCurrencySetting.organization_id == organization_id)
    )
    settings = result.scalar_one_or_none()
    if not settings:
        settings = MultiCurrencySetting(organization_id=organization_id)
        db.add(settings)

    settings.base_currency = base_currency
    settings.allowed_currencies = allowed_currencies or settings.allowed_currencies
    settings.rounding_policy = rounding_policy or settings.rounding_policy
    settings.decimal_places = decimal_places
    settings.auto_update_rates = auto_update_rates
    settings.rate_provider = rate_provider or settings.rate_provider
    settings.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(settings)
    return settings


# Exchange rates
@router.post("/currency/rates")
async def add_rate(
    organization_id: int,
    base_currency: str,
    target_currency: str,
    rate: float,
    source: Optional[str] = None,
    effective_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    rate_row = CurrencyRate(
        organization_id=organization_id,
        base_currency=base_currency,
        target_currency=target_currency,
        rate=rate,
        source=source,
        effective_date=effective_date or datetime.utcnow(),
    )
    db.add(rate_row)
    await db.commit()
    await db.refresh(rate_row)
    return rate_row


@router.get("/currency/rates")
async def list_rates(
    organization_id: int,
    base_currency: Optional[str] = None,
    target_currency: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(CurrencyRate).where(CurrencyRate.organization_id == organization_id)
    if base_currency:
        query = query.where(CurrencyRate.base_currency == base_currency)
    if target_currency:
        query = query.where(CurrencyRate.target_currency == target_currency)
    result = await db.execute(query.order_by(CurrencyRate.effective_date.desc()))
    return result.scalars().all()


@router.post("/currency/convert")
async def convert_amount(
    organization_id: int,
    amount: float,
    from_currency: str,
    to_currency: str,
    db: AsyncSession = Depends(get_db),
):
    rate_result = await db.execute(
        select(CurrencyRate)
        .where(
            CurrencyRate.organization_id == organization_id,
            CurrencyRate.base_currency == from_currency,
            CurrencyRate.target_currency == to_currency,
        )
        .order_by(CurrencyRate.effective_date.desc())
    )
    rate_row = rate_result.scalars().first()
    if not rate_row:
        raise HTTPException(status_code=404, detail="Rate not found")

    converted = amount * rate_row.rate
    log = CurrencyConversionLog(
        organization_id=organization_id,
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        converted_amount=converted,
        rate_used=rate_row.rate,
    )
    db.add(log)
    await db.commit()
    return {"converted_amount": converted, "rate_used": rate_row.rate}


# Localization profiles
@router.post("/profiles")
async def create_profile(
    organization_id: int,
    name: str,
    locale: str = "en-US",
    time_zone: str = "UTC",
    date_format: str = "YYYY-MM-DD",
    number_format: str = "1,234.56",
    first_day_of_week: str = "Monday",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(LocalizationProfile.id)))
    count = result.scalar() or 0
    profile_code = f"LOC-{count + 1:04d}"

    profile = LocalizationProfile(
        organization_id=organization_id,
        profile_code=profile_code,
        name=name,
        locale=locale,
        time_zone=time_zone,
        date_format=date_format,
        number_format=number_format,
        first_day_of_week=first_day_of_week,
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("/profiles")
async def list_profiles(organization_id: int, locale: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(LocalizationProfile).where(LocalizationProfile.organization_id == organization_id)
    if locale:
        query = query.where(LocalizationProfile.locale == locale)
    result = await db.execute(query)
    return result.scalars().all()


# Language resources
@router.post("/languages/resources")
async def upsert_language_resource(
    organization_id: int,
    key: str,
    locale: str,
    text: str,
    context: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(LanguageResource).where(
            LanguageResource.organization_id == organization_id,
            LanguageResource.key == key,
            LanguageResource.locale == locale,
        )
    )
    res = result.scalar_one_or_none()
    if not res:
        res = LanguageResource(
            organization_id=organization_id,
            key=key,
            locale=locale,
        )
        db.add(res)

    res.text = text
    res.context = context
    res.last_updated = datetime.utcnow()

    await db.commit()
    await db.refresh(res)
    return res


# Analytics
@router.get("/analytics/currency-coverage")
async def currency_coverage(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Report how many rates exist per base currency."""
    result = await db.execute(
        select(CurrencyRate.base_currency, func.count(CurrencyRate.id))
        .where(CurrencyRate.organization_id == organization_id)
        .group_by(CurrencyRate.base_currency)
    )
    return {row[0]: row[1] for row in result.all()}
