"""IoT (Internet of Things) Integration Models (Dynamics 365 parity)."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text

from dario_app.database import Base


class IoTDevice(Base):
    """Connected IoT devices for monitoring and predictive maintenance."""
    __tablename__ = "iot_devices"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    device_code = Column(String(50), unique=True, nullable=False)
    
    device_name = Column(String(255), nullable=False)
    device_type = Column(String(50), nullable=False)  # Sensor, Gateway, Smart_Equipment, Vehicle, Environmental
    manufacturer = Column(String(255))
    model_number = Column(String(100))
    serial_number = Column(String(100), unique=True)
    
    # Location & asset
    asset_id = Column(String(36))  # FK to Asset
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Connection
    connection_type = Column(String(50))  # WiFi, Cellular, Bluetooth, LoRaWAN, NB-IoT, Ethernet
    device_ip = Column(String(50))
    mac_address = Column(String(50), unique=True)
    device_identifier = Column(String(100), unique=True)  # Unique device ID
    
    # Status
    status = Column(String(50), default="Active")  # Active, Inactive, Disabled, Decommissioned
    last_seen = Column(DateTime)
    connection_status = Column(String(50))  # Connected, Disconnected, Low_Signal, Error
    battery_level = Column(Float)  # Percentage (0-100)
    signal_strength = Column(Float)  # dBm
    
    # Device configuration
    firmware_version = Column(String(50))
    last_firmware_update = Column(DateTime)
    configuration = Column(JSON)  # Device-specific configuration
    
    # Capabilities
    sensor_types = Column(JSON, default=[])  # ['Temperature', 'Humidity', 'Vibration', 'Pressure']
    capabilities = Column(JSON, default=[])  # ['Real-time_monitoring', 'Predictive_analytics']
    
    # Maintenance
    install_date = Column(DateTime)
    last_maintenance_date = Column(DateTime)
    next_maintenance_date = Column(DateTime)
    maintenance_history = Column(JSON, default=[])
    
    # Data collection
    data_collection_interval = Column(Integer)  # Seconds
    total_readings = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DeviceReading(Base):
    """IoT sensor readings and telemetry data."""
    __tablename__ = "device_readings"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    device_id = Column(String(36), nullable=False, index=True)
    
    reading_type = Column(String(50), nullable=False)  # Temperature, Humidity, Pressure, Vibration, RPM, Power
    reading_timestamp = Column(DateTime, nullable=False, index=True)
    
    # Reading values
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)  # C, F, %, psi, Hz, kW
    
    # Status & Quality
    reading_status = Column(String(50), default="Valid")  # Valid, Invalid, Suspect, Error
    quality_score = Column(Float, default=100.0)  # 0-100%
    
    # Anomaly detection
    is_anomalous = Column(Boolean, default=False)
    anomaly_score = Column(Float)
    
    # Raw data
    raw_data = Column(JSON)  # Additional sensor data
    
    # Device context at time of reading
    device_status = Column(String(50))  # Operating, Idle, Error
    battery_level = Column(Float)  # Percentage
    signal_strength = Column(Float)  # dBm
    
    created_at = Column(DateTime, default=datetime.utcnow)


class AlertRule(Base):
    """Alert rules for IoT device monitoring and thresholds."""
    __tablename__ = "iot_alert_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    alert_code = Column(String(50), unique=True, nullable=False)
    
    rule_name = Column(String(255), nullable=False)
    description = Column(Text)
    rule_type = Column(String(50), nullable=False)  # Threshold, Anomaly, Predictive, Connectivity
    
    # Scope
    device_id = Column(String(36))  # Can be null for all devices
    device_type = Column(String(50))  # Can be null for all types
    reading_type = Column(String(50))
    
    # Conditions
    condition_logic = Column(String(50))  # Greater_Than, Less_Than, Between, Equals, Not_Equals
    lower_threshold = Column(Float)
    upper_threshold = Column(Float)
    
    # Advanced conditions
    duration_trigger = Column(Integer)  # Seconds - alert only if threshold exceeded for this long
    sample_count = Column(Integer)  # Number of samples to evaluate
    
    # Actions
    alert_severity = Column(String(50), default="Medium")  # Critical, High, Medium, Low, Info
    notification_channels = Column(JSON, default=[])  # ['Email', 'SMS', 'Push', 'MQTT']
    recipients = Column(JSON, default=[])  # List of user IDs
    
    # Integration
    create_work_order = Column(Boolean, default=False)
    work_order_template = Column(String(36))
    create_incident = Column(Boolean, default=False)
    
    # Status & metrics
    status = Column(String(50), default="Active")  # Active, Inactive, Disabled
    is_enabled = Column(Boolean, default=True)
    
    # Metrics
    total_alerts_triggered = Column(Integer, default=0)
    last_alert_date = Column(DateTime)
    alert_frequency = Column(Float)  # Alerts per day
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MaintenancePrediction(Base):
    """Predictive maintenance based on IoT data and machine learning."""
    __tablename__ = "maintenance_predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    prediction_code = Column(String(50), unique=True, nullable=False)
    
    device_id = Column(String(36), nullable=False, index=True)
    asset_id = Column(String(36))  # FK to Asset
    
    # Prediction details
    predicted_failure_type = Column(String(255), nullable=False)  # e.g., "Bearing Failure", "Compressor Failure"
    failure_description = Column(Text)
    
    # Timeline prediction
    prediction_date = Column(DateTime, nullable=False)
    predicted_failure_date = Column(DateTime, nullable=False)
    days_to_failure = Column(Integer, nullable=False)
    
    # Confidence & accuracy
    confidence_level = Column(Float, nullable=False)  # 0-100%
    confidence_category = Column(String(50))  # High, Medium, Low
    
    # Risk assessment
    risk_level = Column(String(50))  # Critical, High, Medium, Low
    impact_if_failed = Column(String(50))  # None, Minor, Major, Critical
    
    # Contributing factors
    anomalies_detected = Column(JSON, default=[])  # [{type: 'vibration_spike', count: 5}]
    degradation_trend = Column(JSON)  # Trend analysis
    
    # Recommended action
    recommended_maintenance = Column(String(255))
    maintenance_urgency = Column(String(50))  # Immediate, Soon, Plan_Ahead
    estimated_maintenance_cost = Column(Float)
    
    # Work order
    work_order_id = Column(String(36))
    maintenance_scheduled = Column(Boolean, default=False)
    scheduled_date = Column(DateTime)
    
    # Outcome tracking
    actual_failure_date = Column(DateTime)  # Populated if equipment fails
    maintenance_performed = Column(Boolean, default=False)
    predicted_correctly = Column(Boolean)  # True if prediction was accurate
    
    status = Column(String(50), default="Active")  # Active, Acted_Upon, Expired, Completed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
