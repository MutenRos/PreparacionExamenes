"""
Multi-Channel Communication Hub - Models
Centralizes omni-channel messaging across email, SMS, chat, and social.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from dario_app.database import Base


class CommunicationChannel(Base):
    """Configured communication channel (email, SMS, chat, social, push)."""
    __tablename__ = "comm_channels"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    channel_code = Column(String(50), unique=True, nullable=False, index=True)
    channel_type = Column(String(50), nullable=False)  # Email, SMS, Chat, Social, Push
    provider = Column(String(100))  # Twilio, SendGrid, WhatsApp, Teams
    configuration = Column(JSON)  # API keys, webhook URLs, auth tokens
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    daily_quota = Column(Integer)  # Max messages per day
    rate_limit_per_minute = Column(Integer)
    retry_policy = Column(JSON)  # backoff, max_retries

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))

    templates = relationship("MessageTemplate", back_populates="channel", cascade="all, delete-orphan")
    threads = relationship("ConversationThread", back_populates="channel", cascade="all, delete-orphan")


class MessageTemplate(Base):
    """Reusable message templates per channel."""
    __tablename__ = "comm_templates"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    channel_id = Column(Integer, ForeignKey("comm_channels.id"))

    template_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    subject = Column(String(200))
    body = Column(Text)
    variables = Column(JSON)  # Allowed placeholders
    category = Column(String(100))  # Marketing, Service, Alert
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))

    channel = relationship("CommunicationChannel", back_populates="templates")


class ConversationThread(Base):
    """Conversation thread grouping inbound/outbound messages."""
    __tablename__ = "comm_threads"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    channel_id = Column(Integer, ForeignKey("comm_channels.id"))

    thread_code = Column(String(50), unique=True, nullable=False, index=True)
    subject = Column(String(200))
    customer_id = Column(Integer, index=True)
    contact_point = Column(String(200))  # email/phone/handle
    status = Column(String(50), default="Open")  # Open, Pending, Resolved, Closed
    priority = Column(String(50), default="Normal")  # Low, Normal, High, Urgent
    tags = Column(JSON)

    last_message_at = Column(DateTime)
    last_inbound_at = Column(DateTime)
    last_outbound_at = Column(DateTime)
    unread_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    channel = relationship("CommunicationChannel", back_populates="threads")
    messages = relationship("Message", back_populates="thread", cascade="all, delete-orphan")


class Message(Base):
    """Individual inbound/outbound message."""
    __tablename__ = "comm_messages"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    thread_id = Column(Integer, ForeignKey("comm_threads.id"))

    direction = Column(String(50), nullable=False)  # Inbound, Outbound
    channel_type = Column(String(50))
    provider_message_id = Column(String(100))
    sender = Column(String(200))
    recipient = Column(String(200))
    subject = Column(String(200))
    body = Column(Text)
    attachments = Column(JSON)
    message_metadata = Column("metadata", JSON)  # headers, delivery info

    status = Column(String(50), default="Queued")  # Queued, Sent, Delivered, Read, Failed
    delivery_status = Column(String(50))  # provider specific
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    thread = relationship("ConversationThread", back_populates="messages")


class ContactPreference(Base):
    """Per-contact communication preferences and opt-ins."""
    __tablename__ = "comm_contact_preferences"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    customer_id = Column(Integer, nullable=False, index=True)

    preferred_channels = Column(JSON)  # [Email, SMS, Chat]
    quiet_hours = Column(JSON)  # time windows to avoid
    opt_in_marketing = Column(Boolean, default=False)
    opt_in_service = Column(Boolean, default=True)
    blocked = Column(Boolean, default=False)
    reason = Column(String(200))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(100))
