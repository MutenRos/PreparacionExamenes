"""IoT Integration API routes (Dynamics 365 parity)."""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid

from dario_app.database import get_db

router = APIRouter(prefix="/iot_integration", tags=["IoT Integration"])


class DeviceCreate(BaseModel):
    device_name: str
    device_type: str
    connection_type: str
    location: Optional[str] = None


class ReadingCreate(BaseModel):
    device_id: str
    reading_type: str
    value: float
    unit: str


class AlertRuleCreate(BaseModel):
    rule_name: str
    rule_type: str
    device_id: Optional[str] = None
    reading_type: Optional[str] = None
    condition_logic: str
    lower_threshold: Optional[float] = None
    upper_threshold: Optional[float] = None


@router.post("/devices")
async def create_device(data: DeviceCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Register IoT device."""
    from dario_app.modules.iot_integration.models import IoTDevice
    
    device = IoTDevice(
        organization_id=org_id,
        device_code=f"IOT-{uuid.uuid4().hex[:8].upper()}",
        device_name=data.device_name,
        device_type=data.device_type,
        connection_type=data.connection_type,
        location=data.location,
        status="Active"
    )
    session.add(device)
    await session.commit()
    return {"device_id": device.id, "device_code": device.device_code}


@router.get("/devices")
async def list_devices(session: AsyncSession = Depends(get_db), device_type: Optional[str] = None, status: Optional[str] = None, org_id: str = "default"):
    """List IoT devices."""
    from dario_app.modules.iot_integration.models import IoTDevice
    
    query = select(IoTDevice).where(IoTDevice.organization_id == org_id)
    if device_type:
        query = query.where(IoTDevice.device_type == device_type)
    if status:
        query = query.where(IoTDevice.status == status)
    
    result = await session.execute(query)
    devices = result.scalars().all()
    
    return {
        "total": len(devices),
        "devices": [
            {
                "id": d.id,
                "device_code": d.device_code,
                "device_name": d.device_name,
                "device_type": d.device_type,
                "status": d.status,
                "connection_status": d.connection_status,
                "battery_level": d.battery_level,
                "last_seen": d.last_seen
            }
            for d in devices
        ]
    }


@router.get("/devices/{device_id}")
async def get_device_details(device_id: str, session: AsyncSession = Depends(get_db)):
    """Get device details and current status."""
    from dario_app.modules.iot_integration.models import IoTDevice
    
    device = await session.get(IoTDevice, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return {
        "device_id": device.id,
        "device_code": device.device_code,
        "device_name": device.device_name,
        "device_type": device.device_type,
        "location": device.location,
        "status": device.status,
        "connection_status": device.connection_status,
        "battery_level": device.battery_level,
        "signal_strength": device.signal_strength,
        "firmware_version": device.firmware_version,
        "total_readings": device.total_readings,
        "last_seen": device.last_seen
    }


@router.post("/readings")
async def create_reading(data: ReadingCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Record IoT sensor reading."""
    from dario_app.modules.iot_integration.models import DeviceReading, IoTDevice
    
    # Verify device exists
    device = await session.get(IoTDevice, data.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    reading = DeviceReading(
        organization_id=org_id,
        device_id=data.device_id,
        reading_type=data.reading_type,
        value=data.value,
        unit=data.unit,
        reading_timestamp=datetime.utcnow(),
        reading_status="Valid"
    )
    session.add(reading)
    device.total_readings += 1
    device.last_seen = datetime.utcnow()
    
    await session.commit()
    return {"reading_id": reading.id, "status": "recorded"}


@router.get("/readings/{device_id}")
async def get_device_readings(device_id: str, session: AsyncSession = Depends(get_db), limit: int = Query(100, le=1000)):
    """Get latest readings from a device."""
    from dario_app.modules.iot_integration.models import DeviceReading
    
    query = select(DeviceReading).where(
        DeviceReading.device_id == device_id
    ).order_by(DeviceReading.reading_timestamp.desc()).limit(limit)
    
    result = await session.execute(query)
    readings = result.scalars().all()
    
    return {
        "device_id": device_id,
        "total_readings": len(readings),
        "readings": [
            {
                "reading_id": r.id,
                "reading_type": r.reading_type,
                "value": r.value,
                "unit": r.unit,
                "timestamp": r.reading_timestamp,
                "status": r.reading_status,
                "is_anomalous": r.is_anomalous,
                "anomaly_score": r.anomaly_score
            }
            for r in readings
        ]
    }


@router.post("/alert-rules")
async def create_alert_rule(data: AlertRuleCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create alert rule for device monitoring."""
    from dario_app.modules.iot_integration.models import AlertRule
    
    rule = AlertRule(
        organization_id=org_id,
        alert_code=f"ALR-{uuid.uuid4().hex[:8].upper()}",
        rule_name=data.rule_name,
        rule_type=data.rule_type,
        device_id=data.device_id,
        reading_type=data.reading_type,
        condition_logic=data.condition_logic,
        lower_threshold=data.lower_threshold,
        upper_threshold=data.upper_threshold
    )
    session.add(rule)
    await session.commit()
    return {"rule_id": rule.id, "alert_code": rule.alert_code}


@router.get("/alert-rules")
async def list_alert_rules(session: AsyncSession = Depends(get_db), device_id: Optional[str] = None, org_id: str = "default"):
    """List alert rules."""
    from dario_app.modules.iot_integration.models import AlertRule
    
    query = select(AlertRule).where(AlertRule.organization_id == org_id)
    if device_id:
        query = query.where(AlertRule.device_id == device_id)
    
    result = await session.execute(query)
    rules = result.scalars().all()
    
    return {
        "total": len(rules),
        "rules": [
            {
                "id": r.id,
                "alert_code": r.alert_code,
                "rule_name": r.rule_name,
                "rule_type": r.rule_type,
                "alert_severity": r.alert_severity,
                "status": r.status,
                "total_alerts_triggered": r.total_alerts_triggered
            }
            for r in rules
        ]
    }


@router.get("/maintenance-predictions/{device_id}")
async def get_maintenance_predictions(device_id: str, session: AsyncSession = Depends(get_db)):
    """Get predictive maintenance recommendations for a device."""
    from dario_app.modules.iot_integration.models import MaintenancePrediction
    
    query = select(MaintenancePrediction).where(
        MaintenancePrediction.device_id == device_id
    ).order_by(MaintenancePrediction.prediction_date.desc()).limit(5)
    
    result = await session.execute(query)
    predictions = result.scalars().all()
    
    return {
        "device_id": device_id,
        "total_predictions": len(predictions),
        "predictions": [
            {
                "prediction_id": p.id,
                "predicted_failure_type": p.predicted_failure_type,
                "days_to_failure": p.days_to_failure,
                "confidence_level": p.confidence_level,
                "risk_level": p.risk_level,
                "recommended_maintenance": p.recommended_maintenance
            }
            for p in predictions
        ]
    }


@router.get("/analytics/device-health")
async def get_device_health_analytics(org_id: str = "default"):
    """Get overall IoT fleet health analytics."""
    return {
        "organization_id": org_id,
        "total_devices": 0,
        "active_devices": 0,
        "devices_with_issues": 0,
        "avg_battery_level": 0.0,
        "total_readings_today": 0,
        "devices_needing_maintenance": 0,
        "critical_alerts": 0
    }
